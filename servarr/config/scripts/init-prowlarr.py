#!/usr/local/bin/python3

import os
import json
from utils import post, step, logger

PROWLARR_HOST = os.getenv("PROWLARR_HOST")
API_KEY = os.getenv("API_KEY")
TORRENT_USERNAME = os.getenv("TORRENT_ADMIN")
TORRENT_PASSWORD = os.getenv("TORRENT_PASSWORD")
TORRENT_SERVICE = os.getenv("TORRENT_SERVICE")
PROWLARR_SERVICE = os.getenv("PROWLARR_SERVICE")
RADARR_SERVICE = os.getenv("RADARR_SERVICE")
FLARESOLVERR_SERVICE = os.getenv("FLARESOLVERR_SERVICE")
SONARR_SERVICE = os.getenv("SONARR_SERVICE")


@step("prowlarr_flaresolverr_tags")
def setup_flaresolverr_tags():
    logger.info("Setup Flaresolverr tags in Prowlarr")

    headers = {
        "x-api-key": API_KEY,
        "x-requested-with": "XMLHttpRequest",
    }

    body = {"label": "flare"}

    post(url="http://{}/api/v1/tag".format(PROWLARR_HOST), headers=headers, json=body)


@step("prowlarr_radarr")
def setup_radarr():
    logger.info("Setup Radarr in Prowlarr")

    headers = {
        "x-api-key": API_KEY,
        "x-requested-with": "XMLHttpRequest",
        "X-Prowlarr-Client": "true",
    }

    body = {
        "syncLevel": "fullSync",
        "fields": [
            {"name": "prowlarrUrl", "value": "http://{}".format(PROWLARR_SERVICE)},
            {"name": "baseUrl", "value": "http://{}".format(RADARR_SERVICE)},
            {"name": "apiKey", "value": API_KEY},
            {
                "name": "syncCategories",
                "value": [
                    2000,
                    2010,
                    2020,
                    2030,
                    2040,
                    2045,
                    2050,
                    2060,
                    2070,
                    2080,
                    2090,
                ],
            },
        ],
        "implementationName": "Radarr",
        "implementation": "Radarr",
        "configContract": "RadarrSettings",
        "infoLink": "https://wiki.servarr.com/prowlarr/supported#radarr",
        "tags": [],
        "name": "Radarr",
    }

    post(
        url="http://{}/api/v1/applications".format(PROWLARR_HOST),
        headers=headers,
        json=body,
    )


@step("prowlarr_sonarr")
def setup_sonarr():
    logger.info("Setup Sonarr in Prowlarr")

    headers = {
        "x-api-key": API_KEY,
        "x-requested-with": "XMLHttpRequest",
        "X-Prowlarr-Client": "true",
    }

    body = {
        "syncLevel": "fullSync",
        "fields": [
            {"name": "prowlarrUrl", "value": "http://{}".format(PROWLARR_SERVICE)},
            {"name": "baseUrl", "value": "http://{}".format(SONARR_SERVICE)},
            {"name": "apiKey", "value": API_KEY},
            {
                "name": "syncCategories",
                "value": [5000, 5010, 5020, 5030, 5040, 5045, 5050, 5090],
            },
            {"name": "animeSyncCategories", "value": [5070]},
            {"name": "syncAnimeStandardFormatSearch", "value": False},
        ],
        "implementationName": "Sonarr",
        "implementation": "Sonarr",
        "configContract": "SonarrSettings",
        "infoLink": "https://wiki.servarr.com/prowlarr/supported#sonarr",
        "tags": [],
        "name": "Sonarr",
    }

    post(
        url="http://{}/api/v1/applications".format(PROWLARR_HOST),
        headers=headers,
        json=body,
    )


@step("prowlarr_qbittorrent")
def setup_qbittorrent():
    logger.info("Setup qBitTorrent in Prowlarr")

    headers = {
        "x-api-key": API_KEY,
        "x-requested-with": "XMLHttpRequest",
    }

    body = {
        "enable": True,
        "protocol": "torrent",
        "priority": 1,
        "categories": [],
        "supportsCategories": True,
        "name": "qBittorrent",
        "fields": [
            {"name": "host", "value": TORRENT_SERVICE},
            {"name": "port", "value": "10095"},
            {"name": "useSsl", "value": False},
            {"name": "urlBase"},
            {"name": "username", "value": TORRENT_USERNAME},
            {"name": "password", "value": TORRENT_PASSWORD},
            {"name": "category", "value": "prowlarr"},
            {"name": "priority", "value": 0},
            {"name": "initialState", "value": 0},
            {"name": "sequentialOrder", "value": False},
            {"name": "firstAndLast", "value": False},
            {"name": "contentLayout", "value": 0},
        ],
        "implementationName": "qBittorrent",
        "implementation": "QBittorrent",
        "configContract": "QBittorrentSettings",
        "infoLink": "https://wiki.servarr.com/prowlarr/supported#qbittorrent",
        "tags": [],
    }

    post(
        url="http://{}/api/v1/downloadclient".format(PROWLARR_HOST),
        headers=headers,
        json=body,
    )


@step("prowlarr_flaresolverr")
def setup_flaresolverr():
    logger.info("Setup Flaresolverr in Prowlarr")

    headers = {
        "x-api-key": API_KEY,
        "x-requested-with": "XMLHttpRequest",
    }

    body = {
        "onHealthIssue": False,
        "supportsOnHealthIssue": False,
        "includeHealthWarnings": False,
        "name": "FlareSolverr",
        "fields": [
            {"name": "host", "value": "http://{}/".format(FLARESOLVERR_SERVICE)},
            {"name": "requestTimeout", "value": 60},
        ],
        "implementationName": "FlareSolverr",
        "implementation": "FlareSolverr",
        "configContract": "FlareSolverrSettings",
        "infoLink": "https://wiki.servarr.com/prowlarr/supported#flaresolverr",
        "tags": [1],
    }

    post(
        url="http://{}/api/v1/indexerProxy".format(PROWLARR_HOST),
        headers=headers,
        json=body,
    )


def setup_indexers():
    indexersFile = "/scripts/indexers.json"
    if os.path.isfile(indexersFile):
        logger.info("Setup Prowlarr indexers")

        with open(indexersFile) as file:
            indexers = json.load(file)

        headers = {
            "X-Api-Key": API_KEY,
            "X-Prowlarr-Client": "true",
            "X-Requested-With": "XMLHttpRequest",
        }

        for index in indexers:
            step_name = "prowlarr_indexer_{}".format(index["name"])

            @step(step_name)
            def setup_single_indexer(idx):
                logger.debug("Setup {} index".format(idx["name"]))
                post(
                    url="http://{}/api/v1/indexer".format(PROWLARR_HOST),
                    json=idx["body"],
                    headers=headers,
                )

            setup_single_indexer(index)


setup_flaresolverr_tags()
setup_radarr()
setup_sonarr()
setup_qbittorrent()
setup_flaresolverr()
setup_indexers()
