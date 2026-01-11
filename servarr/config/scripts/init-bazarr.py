#!/usr/local/bin/python3

import json
import os
from utils import post, step, logger

BAZARR_HOST = os.getenv("BAZARR_HOST")
API_KEY = os.getenv("API_KEY")
SONARR_HOST = os.getenv("SONARR_HOST")
SONARR_API_KEY = os.getenv("SONARR_API_KEY")
RADARR_HOST = os.getenv("RADARR_HOST")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")
PREFERRED_SUBTITLES_LANGUAGES = os.getenv("PREFERRED_SUBTITLES_LANGUAGES", "en").split(
    ","
)
PREFERRED_SUBTITLES_PROVIDERS = os.getenv("PREFERRED_SUBTITLES_PROVIDERS", "en").split(
    ","
)


@step("bazarr_subtitles_languages")
def setup_subtitles_languages():
    logger.info(
        "Setup Bazarr subtitles languages: {}".format(PREFERRED_SUBTITLES_LANGUAGES)
    )

    headers = {
        "x-api-key": API_KEY,
    }

    logger.info(
        "Adding preferred subtitle language: {}".format(PREFERRED_SUBTITLES_LANGUAGES)
    )

    body = [("languages-enabled", lang) for lang in PREFERRED_SUBTITLES_LANGUAGES]

    post(
        url="http://{}/api/system/settings".format(BAZARR_HOST),
        headers=headers,
        data=body,
        method="POST",
    )


@step("bazarr_subtitles_languages_profiles")
def setup_subtitles_languages_profiles():
    logger.info(
        "Setup Bazarr subtitles languages: {}".format(PREFERRED_SUBTITLES_LANGUAGES)
    )

    headers = {
        "x-api-key": API_KEY,
    }

    logger.info(
        "Adding preferred subtitle language: {}".format(PREFERRED_SUBTITLES_LANGUAGES)
    )

    body = [
        (
            "languages-profiles",
            json.dumps(
                [
                    {
                        "profileId": 1,
                        "name": "default",
                        "items": [
                            {
                                "id": idx,
                                "language": lang,
                                "audio_exclude": "False",
                                "audio_only_include": "False",
                                "hi": "False",
                                "forced": "False",
                            }
                            for idx, lang in enumerate(
                                PREFERRED_SUBTITLES_LANGUAGES, start=1
                            )
                        ],
                        "cutoff": 65535,
                        "mustContain": [],
                        "mustNotContain": [],
                        "originalFormat": False,
                    }
                ]
            ),
        )
    ]

    post(
        url="http://{}/api/system/settings".format(BAZARR_HOST),
        headers=headers,
        data=body,
        method="POST",
    )


@step("bazarr_subtitles_providers")
def setup_subtitles_providers():
    logger.info(
        "Setup Bazarr subtitles providers: {}".format(PREFERRED_SUBTITLES_PROVIDERS)
    )

    headers = {
        "x-api-key": API_KEY,
    }

    logger.info(
        "Adding preferred subtitle languages: {}".format(PREFERRED_SUBTITLES_PROVIDERS)
    )

    body = [
        ("settings-general-enabled_providers", provider)
        for provider in PREFERRED_SUBTITLES_PROVIDERS
    ]

    post(
        url="http://{}/api/system/settings".format(BAZARR_HOST),
        headers=headers,
        data=body,
        method="POST",
    )


@step("bazarr_sonarr")
def setup_sonarr():
    if not SONARR_HOST or not SONARR_API_KEY:
        logger.info("Sonarr host or API key not provided, skipping integration")
        return

    logger.info("Setup Sonarr integration in Bazarr")

    headers = {
        "x-api-key": API_KEY,
    }

    body = {
        "settings-general-use_sonarr": "true",
        "settings-sonarr-ip": SONARR_HOST.split(":")[0],
        "settings-sonarr-port": int(SONARR_HOST.split(":")[1])
        if ":" in SONARR_HOST
        else 8989,
        "settings-sonarr-apikey": SONARR_API_KEY,
        "settings-sonarr-ssl": "false",
        "settings-sonarr-basepath": "",
    }

    post(
        url="http://{}/api/system/settings".format(BAZARR_HOST),
        headers=headers,
        data=body,
        method="POST",
    )


@step("bazarr_radarr")
def setup_radarr():
    if not RADARR_HOST or not RADARR_API_KEY:
        logger.info("Radarr host or API key not provided, skipping integration")
        return

    logger.info("Setup Radarr integration in Bazarr")

    headers = {
        "x-api-key": API_KEY,
    }

    body = {
        "settings-general-use_radarr": "true",
        "settings-radarr-ip": RADARR_HOST.split(":")[0],
        "settings-radarr-port": int(RADARR_HOST.split(":")[1])
        if ":" in RADARR_HOST
        else 7878,
        "settings-radarr-apikey": RADARR_API_KEY,
        "settings-radarr-ssl": "false",
        "settings-radarr-basepath": "",
    }

    post(
        url="http://{}/api/system/settings".format(BAZARR_HOST),
        headers=headers,
        data=body,
        method="POST",
    )


if __name__ == "__main__":
    setup_subtitles_languages()
    setup_subtitles_languages_profiles()
    setup_subtitles_providers()
    setup_sonarr()
    setup_radarr()
