#!/usr/local/bin/python3

import base64
import hashlib
import os
import sys
from utils import step, logger

MIN_PASS_LEN = 8
QBITTORRENT_CONF_FILENAME = "qBittorrent.conf"
QBITTORRENT_CONF_FILEPATH = "/mnt/qBittorrent"
QBITTORRENT_CONF_ABSOLUTE_PATH = (
    QBITTORRENT_CONF_FILEPATH + os.sep + QBITTORRENT_CONF_FILENAME
)


def create_file(file_content: str):
    os.umask(0o077)
    with open(QBITTORRENT_CONF_ABSOLUTE_PATH, "w+") as fd:
        fd.write(file_content)


def qbittorrent_passwd(plain_passwd: str):
    # As per https://github.com/qbittorrent/qBittorrent/blob/ce9bdaef5cdb8ab77d71481f20b25c9e6da1b9eb/src/base/utils/password.cpp#L48
    ITERATIONS = 100_000
    # 4x32 bits words = 16 bytes: https://github.com/qbittorrent/qBittorrent/blob/ce9bdaef5cdb8ab77d71481f20b25c9e6da1b9eb/src/base/utils/password.cpp#L75
    SALT_SIZE = 16
    # Generate a cryptographically secure pseudorandom salt
    salt = os.urandom(SALT_SIZE)
    # PBKDF2 w/ SHA512 hmac
    h = hashlib.pbkdf2_hmac("sha512", plain_passwd.encode(), salt, ITERATIONS)
    # Base64 encode and join salt and hash
    return (
        f"@ByteArray({base64.b64encode(salt).decode()}:{base64.b64encode(h).decode()})"
    )


TORRENT_USERNAME = os.getenv("TORRENT_USERNAME", "admin")
TORRENT_PASSWORD = os.getenv("TORRENT_PASSWORD", "password")

logger.info("qBitTorrent Init Job started")
logger.info("The Job will configure qBitTorrent credentials")


@step("qbittorrent_generate_config")
def generate_config():
    logger.info("Checking credentials")
    if TORRENT_USERNAME in [None, ""]:
        logger.error("Empty username passed")
        sys.exit(1)
    if TORRENT_PASSWORD in [None, ""]:
        logger.error("Empty password passed")
        sys.exit(1)
    if len(TORRENT_PASSWORD) < MIN_PASS_LEN:
        logger.error("Password too short, it should be at least of 8 characters")
        sys.exit(1)

    logger.info("Username to be set: {0}".format(TORRENT_USERNAME))
    hidden_password = (
        TORRENT_PASSWORD[0] + "*" * (len(TORRENT_PASSWORD) - 2) + TORRENT_PASSWORD[-1]
    )
    logger.info("Password (hidden) to be set: {0}".format(hidden_password))

    logger.info("Generating qBitTorrent compliant hashed password")
    try:
        hashed_password = qbittorrent_passwd(TORRENT_PASSWORD)
    except Exception:
        logger.exception("There was an error while generating the hashed password")
        sys.exit(1)
    logger.info("Hashed password: {0}".format(hashed_password))

    logger.info("Parsing the configuration template")

    conf_rendered = f'''
[Application]
FileLogger\\Age=1
FileLogger\\AgeType=1
FileLogger\\Backup=true
FileLogger\\DeleteOld=true
FileLogger\\Enabled=true
FileLogger\\MaxSizeBytes=66560
FileLogger\\Path=/config/qBittorrent/logs

[BitTorrent]

Session\\DefaultSavePath=/downloads
Session\\ExcludedFileNames=
Session\\Port=50413
Session\\QueueingSystemEnabled=true
Session\\TempPath=/downloads/temp
Session\\GlobalMaxRatio=1.5
Session\\GlobalMaxInactiveSeedingMinutes=120
Session\\GlobalMaxSeedingMinutes=120
Session\\ShareLimitAction=StopActionIndex

[Core]
AutoDeleteAddedTorrentFile=Never

[LegalNotice]
Accepted=true

[Meta]
MigrationVersion=8

[Network]
Proxy\\HostnameLookupEnabled=false
Proxy\\Profiles\\BitTorrent=true
Proxy\\Profiles\\Misc=true
Proxy\\Profiles\\RSS=true

[Preferences]
General\\Locale=en
MailNotification\\req_auth=true
WebUI\\HostHeaderValidation=false
{{- if eq .Values.global.authMethod "External" }}
WebUI\\AuthSubnetWhitelistEnabled=true
WebUI\\AuthSubnetWhitelist=0.0.0.0/0
{{- end }}
{{- if not (default .Values.qbittorrent.csrf_protection false) }}
WebUI\\CSRFProtection=false
WebUI\\ClickjackingProtection=false
{{- end }}
WebUI\\Password_PBKDF2="{hashed_password}"
WebUI\\UseUPnP=false
WebUI\\Username={TORRENT_USERNAME}

[RSS]
AutoDownloader\\DownloadRepacks=true
'''

    logger.info("Rendered configuration file:\n\n{0}\n\n".format(conf_rendered))

    logger.info("Checking if target directory exists")

    if not os.path.exists(QBITTORRENT_CONF_FILEPATH):
        logger.warning(
            "{0} does not exists, will create it".format(QBITTORRENT_CONF_FILEPATH)
        )
        try:
            os.makedirs(QBITTORRENT_CONF_FILEPATH)
        except Exception:
            logger.exception(
                "Could not create directory: {0}".format(QBITTORRENT_CONF_FILEPATH)
            )
            sys.exit(1)

    logger.info("Saving file to PVC")
    try:
        create_file(conf_rendered)
    except Exception:
        logger.exception("Could not create file")
        sys.exit(1)

    logger.info("Setting permissions on files and folders")

    try:
        # Not the pythonic way, but the simplest
        os.system("chown -R 568:568 /mnt/")
        os.system(f"chmod 0644 {QBITTORRENT_CONF_ABSOLUTE_PATH}")
    except Exception:
        logger.exception("Error while setting permissions")
        sys.exit(1)


generate_config()

logger.info("Job ended.")
