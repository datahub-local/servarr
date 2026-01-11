#!/usr/local/bin/python3

import os
from utils import post, step, logger

RADARR_HOST = os.getenv("RADARR_HOST")
API_KEY = os.getenv("API_KEY")
TORRENT_SERVICE = os.getenv("TORRENT_SERVICE")
TORRENT_USERNAME = os.getenv("TORRENT_ADMIN")
TORRENT_PASSWORD = os.getenv("TORRENT_PASSWORD")
LIBRARY_PATH = os.getenv("LIBRARY_PATH", "/mnt/media/library")


@step("radarr_qbittorrent")
def setup_qbittorrent():
    logger.info("Setup qBitTorrent in Radarr")

    headers = {
        "x-api-key": API_KEY,
        "x-requested-with": "XMLHttpRequest",
    }

    body = {
        "enable": True,
        "protocol": "torrent",
        "priority": 1,
        "removeCompletedDownloads": True,
        "removeFailedDownloads": True,
        "name": "qBittorrent",
        "fields": [
            {"name": "host", "value": TORRENT_SERVICE},
            {"name": "port", "value": "10095"},
            {"name": "useSsl", "value": False},
            {"name": "urlBase"},
            {"name": "username", "value": TORRENT_USERNAME},
            {"name": "password", "value": TORRENT_PASSWORD},
            {"name": "movieCategory", "value": "radarr"},
            {"name": "movieImportedCategory"},
            {"name": "recentMoviePriority", "value": 0},
            {"name": "olderMoviePriority", "value": 0},
            {"name": "initialState", "value": 0},
            {"name": "sequentialOrder", "value": False},
            {"name": "firstAndLast", "value": False},
            {"name": "contentLayout", "value": 0},
        ],
        "implementationName": "qBittorrent",
        "implementation": "QBittorrent",
        "configContract": "QBittorrentSettings",
        "infoLink": "https://wiki.servarr.com/radarr/supported#qbittorrent",
        "tags": [],
    }

    post(
        url="http://{}/api/v3/downloadclient".format(RADARR_HOST),
        headers=headers,
        json=body,
    )


@step("radarr_remote_path_mapping")
def setup_remote_path_mapping():
    logger.info("Setup Remote Path Mapping")

    headers = {
        "x-api-key": API_KEY,
        "x-requested-with": "XMLHttpRequest",
    }

    body = {
        "host": TORRENT_SERVICE,
        "remotePath": "/downloads",
        "localPath": "/mnt/downloads/",
    }

    post(
        url="http://{}/api/v3/remotepathmapping".format(RADARR_HOST),
        headers=headers,
        json=body,
    )


@step("radarr_root_folder")
def setup_root_folder():
    logger.info("Setup Root Folder")

    headers = {
        "x-api-key": API_KEY,
        "x-requested-with": "XMLHttpRequest",
    }

    body = {"path": "{}/".format(LIBRARY_PATH)}

    post(
        url="http://{}/api/v3/rootFolder".format(RADARR_HOST),
        headers=headers,
        json=body,
    )


@step("radarr_media_management")
def setup_media_management():
    headers = {
        "x-api-key": API_KEY,
        "x-requested-with": "XMLHttpRequest",
    }

    body = {
        "autoUnmonitorPreviouslyDownloadedMovies": False,
        "recycleBin": "",
        "recycleBinCleanupDays": 7,
        "downloadPropersAndRepacks": "preferAndUpgrade",
        "createEmptyMovieFolders": False,
        "deleteEmptyFolders": False,
        "fileDate": "none",
        "rescanAfterRefresh": "always",
        "autoRenameFolders": False,
        "pathsDefaultStatic": False,
        "setPermissionsLinux": False,
        "chmodFolder": "755",
        "chownGroup": "",
        "skipFreeSpaceCheckWhenImporting": False,
        "minimumFreeSpaceWhenImporting": 100,
        "copyUsingHardlinks": False,
        "useScriptImport": False,
        "scriptImportPath": "",
        "importExtraFiles": False,
        "extraFileExtensions": "srt",
        "enableMediaInfo": True,
        "id": 1,
    }

    post(
        url="http://{}/api/v3/config/mediamanagement".format(RADARR_HOST),
        headers=headers,
        json=body,
        method="PUT",
    )


setup_qbittorrent()
setup_remote_path_mapping()
setup_root_folder()
setup_media_management()
