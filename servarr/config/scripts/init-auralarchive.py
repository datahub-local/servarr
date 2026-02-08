#!/usr/local/bin/python3

import os
from utils import post, get, step, logger

AURALARCHIVE_HOST = os.getenv("AURALARCHIVE_HOST")
AUDIOBOOKSHELF_HOST = os.getenv("AUDIOBOOKSHELF_HOST")
AUDIOBOOKSHELF_API_KEY = os.getenv("AUDIOBOOKSHELF_API_KEY", "")
QBITTORRENT_HOST = os.getenv("QBITTORRENT_HOST")
QBITTORRENT_USERNAME = os.getenv("QBITTORRENT_USERNAME")
QBITTORRENT_PASSWORD = os.getenv("QBITTORRENT_PASSWORD")


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
    configure_audiobookshelf()
    test_audiobookshelf()
    configure_download_client()
    test_download_client()
    configure_media_management()
