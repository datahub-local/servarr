#!/usr/local/bin/python3

import os
from utils import post, step, logger

AUDIOBOOKSHELF_HOST = os.getenv("AUDIOBOOKSHELF_HOST")
AUDIOBOOKSHELF_USERNAME = os.getenv("AUDIOBOOKSHELF_USERNAME")
AUDIOBOOKSHELF_PASSWORD = os.getenv("AUDIOBOOKSHELF_PASSWORD")
AUDIOBOOKS_PATH = os.getenv("AUDIOBOOKS_PATH", "/audiobooks")
METADATA_PATH = os.getenv("METADATA_PATH", "/metadata")


@step("audiobookshelf_setup_root_user")
def setup_root_user():
    """Create the initial admin user via the Audiobookshelf setup API."""
    logger.info(
        "Setting up Audiobookshelf root user: {}".format(AUDIOBOOKSHELF_USERNAME)
    )

    body = {
        "newRoot": {
            "username": AUDIOBOOKSHELF_USERNAME,
            "password": AUDIOBOOKSHELF_PASSWORD,
        }
    }

    post(
        url="http://{}/init".format(AUDIOBOOKSHELF_HOST),
        headers={},
        json=body,
    )
    
    logger.info("Root user created successfully, token obtained")


@step("audiobookshelf_login")
def login():
    """Login to get an auth token for subsequent API calls."""
    logger.info("Logging into Audiobookshelf")

    body = {
        "username": AUDIOBOOKSHELF_USERNAME,
        "password": AUDIOBOOKSHELF_PASSWORD,
    }

    result = post(
        url="http://{}/login".format(AUDIOBOOKSHELF_HOST),
        headers={},
        json=body,
    )

    return result


def get_auth_token():
    """Helper to get auth token by logging in."""
    body = {
        "username": AUDIOBOOKSHELF_USERNAME,
        "password": AUDIOBOOKSHELF_PASSWORD,
    }

    result = post(
        url="http://{}/login".format(AUDIOBOOKSHELF_HOST),
        headers={},
        json=body,
    )

    token = result.get("response", {}).get("user", {}).get("token")
    if not token:
        raise Exception("Failed to obtain auth token from Audiobookshelf")

    return token


@step("audiobookshelf_create_library")
def create_library():
    """Create the audiobooks library."""
    logger.info("Creating Audiobookshelf audiobooks library")

    token = get_auth_token()
    headers = {
        "Authorization": "Bearer {}".format(token),
    }

    body = {
        "name": "Audiobooks",
        "folders": [{"fullPath": AUDIOBOOKS_PATH}],
        "mediaType": "book",
        "provider": "audible",
        "settings": {
            "coverAspectRatio": 1,
            "disableWatcher": False,
            "skipMatchingMediaWithAsin": False,
            "skipMatchingMediaWithIsbn": False,
            "autoScanCronExpression": "0 0 * * *",
            "metadataPath": METADATA_PATH,
        },
    }

    post(
        url="http://{}/api/libraries".format(AUDIOBOOKSHELF_HOST),
        headers=headers,
        json=body,
    )

    logger.info("Audiobooks library created successfully")


if __name__ == "__main__":
    setup_root_user()
    login()
    create_library()
