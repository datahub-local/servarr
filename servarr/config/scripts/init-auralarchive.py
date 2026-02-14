#!/usr/local/bin/python3

import os
from utils import post, step, logger

AURALARCHIVE_HOST = os.getenv("AURALARCHIVE_HOST")
AURALARCHIVE_USERNAME = os.getenv("AURALARCHIVE_USERNAME")
AURALARCHIVE_PASSWORD = os.getenv("AURALARCHIVE_PASSWORD")
AUDIOBOOKSHELF_HOST = os.getenv("AUDIOBOOKSHELF_HOST")
AUDIOBOOKSHELF_API_KEY = os.getenv("AUDIOBOOKSHELF_API_KEY", "")
QBITTORRENT_HOST = os.getenv("QBITTORRENT_HOST")
QBITTORRENT_USERNAME = os.getenv("QBITTORRENT_USERNAME")
QBITTORRENT_PASSWORD = os.getenv("QBITTORRENT_PASSWORD")


@step("auralarchive_setup_user")
def setup_user():
    """Create initial admin user in AuralArchive, matching Jellyfin init behavior."""
    if not AURALARCHIVE_USERNAME or not AURALARCHIVE_PASSWORD:
        logger.info(
            "AuralArchive admin credentials not configured, skipping user setup"
        )
        return

    logger.info("Setting up AuralArchive admin user")

    body = {
        "username": AURALARCHIVE_USERNAME,
        "password": AURALARCHIVE_PASSWORD,
        "confirm_password": AURALARCHIVE_PASSWORD,
        "accept_terms": "on",
    }

    post(
        url="http://{}/auth/setup".format(AURALARCHIVE_HOST),
        headers={},
        data=body,
    )

    logger.info("AuralArchive admin user setup completed")


@step("auralarchive_configure_audiobookshelf")
def configure_audiobookshelf():
    """Configure AudioBookShelf integration in AuralArchive."""
    if not AUDIOBOOKSHELF_HOST:
        logger.info("AudioBookShelf host not configured, skipping integration")
        return

    logger.info(
        "Configuring AudioBookShelf integration: {}".format(AUDIOBOOKSHELF_HOST)
    )

    body = {
        "abs_host": "http://{}".format(AUDIOBOOKSHELF_HOST),
        "abs_api_key": AUDIOBOOKSHELF_API_KEY,
        "abs_enabled": True,
        "abs_sync_metadata": True,
        "abs_sync_only_owned": False,
        "abs_auto_sync": True,
        "abs_sync_frequency": "30min",
        "abs_auto_match_imports": True,
        "abs_auto_match_delay_seconds": 10,
        "library_path": "/audiobooks",
        "naming_template": "series-aware",
    }

    post(
        url="http://{}/settings/api/audiobookshelf/config".format(AURALARCHIVE_HOST),
        headers={},
        json=body,
    )

    logger.info("AudioBookShelf integration configured successfully")


@step("auralarchive_test_audiobookshelf")
def test_audiobookshelf():
    """Test the AudioBookShelf connection."""
    if not AUDIOBOOKSHELF_HOST:
        logger.info("AudioBookShelf host not configured, skipping test")
        return

    logger.info("Testing AudioBookShelf connection")

    body = {
        "abs_host": "http://{}".format(AUDIOBOOKSHELF_HOST),
        "abs_api_key": AUDIOBOOKSHELF_API_KEY,
    }

    result = post(
        url="http://{}/settings/api/test-audiobookshelf".format(AURALARCHIVE_HOST),
        headers={},
        json=body,
    )

    logger.info("AudioBookShelf connection test result: {}".format(result))


@step("auralarchive_configure_download_client")
def configure_download_client():
    """Configure qBittorrent as the download client."""
    if not QBITTORRENT_HOST:
        logger.info("qBittorrent host not configured, skipping")
        return

    logger.info("Configuring qBittorrent download client: {}".format(QBITTORRENT_HOST))

    host_parts = QBITTORRENT_HOST.split(":")
    qbt_host = host_parts[0]
    qbt_port = int(host_parts[1]) if len(host_parts) > 1 else 10095

    body = {
        "download_client": {
            "type": "qbittorrent",
            "host": qbt_host,
            "port": qbt_port,
            "username": QBITTORRENT_USERNAME,
            "password": QBITTORRENT_PASSWORD,
            "category": "audiobooks",
            "enabled": True,
            "auto_download": True,
        }
    }

    post(
        url="http://{}/settings/api/config/save".format(AURALARCHIVE_HOST),
        headers={},
        json=body,
    )

    logger.info("Download client configured successfully")


@step("auralarchive_test_download_client")
def test_download_client():
    """Test the download client connection."""
    if not QBITTORRENT_HOST:
        logger.info("qBittorrent host not configured, skipping test")
        return

    logger.info("Testing qBittorrent connection")

    host_parts = QBITTORRENT_HOST.split(":")
    qbt_host = host_parts[0]
    qbt_port = int(host_parts[1]) if len(host_parts) > 1 else 10095

    body = {
        "type": "qbittorrent",
        "host": qbt_host,
        "port": qbt_port,
        "username": QBITTORRENT_USERNAME,
        "password": QBITTORRENT_PASSWORD,
    }

    result = post(
        url="http://{}/settings/api/test-download-client".format(AURALARCHIVE_HOST),
        headers={},
        json=body,
    )

    logger.info("Download client connection test result: {}".format(result))


@step("auralarchive_enable_automatic_downloads")
def enable_automatic_downloads():
    """Enable automatic downloads in AuralArchive search automation settings."""
    if not QBITTORRENT_HOST:
        logger.info("qBittorrent host not configured, skipping automatic downloads")
        return

    logger.info("Enabling automatic downloads")

    body = {
        "auto_download_enabled": True,
    }

    post(
        url="http://{}/settings/api/search/config".format(AURALARCHIVE_HOST),
        headers={},
        json=body,
    )

    logger.info("Automatic downloads enabled")


@step("auralarchive_configure_media_management")
def configure_media_management():
    """Configure media management paths."""
    logger.info("Configuring media management settings")

    body = {
        "downloads_path": "/downloads",
        "library_path": "/audiobooks",
        "import_path": "/import",
    }

    post(
        url="http://{}/settings/api/media-management".format(AURALARCHIVE_HOST),
        headers={},
        json=body,
    )

    logger.info("Media management configured successfully")


if __name__ == "__main__":
    setup_user()
    configure_audiobookshelf()
    test_audiobookshelf()
    configure_download_client()
    test_download_client()
    enable_automatic_downloads()
    configure_media_management()
