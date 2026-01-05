#!/usr/local/bin/python3

import os
from utils import post, get, step, logger

JELLYFIN_HOST = os.getenv("JELLYFIN_HOST")
JELLYFIN_USERNAME = os.getenv("JELLYFIN_USERNAME")
JELLYFIN_PASSWORD = os.getenv("JELLYFIN_PASSWORD")
COUNTRY_CODE = os.getenv("COUNTRY_CODE")
PREFERRED_LANGUAGE = os.getenv("PREFERRED_LANGUAGE")


def setup_location_logic():
    logger.info("Setup Location")

    headers = {"Content-Type": "application/json"}

    body = {
        "UICulture": "en-US",
        "MetadataCountryCode": COUNTRY_CODE,
        "PreferredMetadataLanguage": PREFERRED_LANGUAGE,
    }

    post(
        url="http://{}/Startup/Configuration".format(JELLYFIN_HOST),
        headers=headers,
        body=body,
    )


@step("jellyfin_setup_location_1")
def setup_location_1():
    setup_location_logic()


@step("jellyfin_setup_user")
def setup_user():
    headers = {"Content-Type": "application/json"}
    logger.info("Ping GET user endpoint")

    get(url="http://{}/Startup/User".format(JELLYFIN_HOST), headers=headers)

    logger.info("Setup the new user")

    body = {"Name": JELLYFIN_USERNAME, "Password": JELLYFIN_PASSWORD}

    post(url="http://{}/Startup/User".format(JELLYFIN_HOST), headers=headers, body=body)


@step("jellyfin_setup_library")
def setup_library():
    headers = {"Content-Type": "application/json"}
    logger.info("Setup the library")

    body = {
        "LibraryOptions": {
            "EnableArchiveMediaFiles": False,
            "EnablePhotos": True,
            "EnableRealtimeMonitor": False,
            "ExtractChapterImagesDuringLibraryScan": True,
            "EnableChapterImageExtraction": True,
            "EnableInternetProviders": True,
            "SaveLocalMetadata": True,
            "EnableAutomaticSeriesGrouping": False,
            "PreferredMetadataLanguage": PREFERRED_LANGUAGE,
            "MetadataCountryCode": COUNTRY_CODE,
            "SeasonZeroDisplayName": "Specials",
            "AutomaticRefreshIntervalDays": 0,
            "EnableEmbeddedTitles": False,
            "EnableEmbeddedEpisodeInfos": False,
            "AllowEmbeddedSubtitles": "AllowAll",
            "SkipSubtitlesIfEmbeddedSubtitlesPresent": False,
            "SkipSubtitlesIfAudioTrackMatches": False,
            "SaveSubtitlesWithMedia": True,
            "RequirePerfectSubtitleMatch": True,
            "AutomaticallyAddToCollection": False,
            "MetadataSavers": [],
            "TypeOptions": [
                {
                    "Type": "Series",
                    "MetadataFetchers": ["TheMovieDb", "The Open Movie Database"],
                    "MetadataFetcherOrder": ["TheMovieDb", "The Open Movie Database"],
                    "ImageFetchers": ["TheMovieDb"],
                    "ImageFetcherOrder": ["TheMovieDb"],
                },
                {
                    "Type": "Season",
                    "MetadataFetchers": ["TheMovieDb"],
                    "MetadataFetcherOrder": ["TheMovieDb"],
                    "ImageFetchers": ["TheMovieDb"],
                    "ImageFetcherOrder": ["TheMovieDb"],
                },
                {
                    "Type": "Episode",
                    "MetadataFetchers": ["TheMovieDb", "The Open Movie Database"],
                    "MetadataFetcherOrder": ["TheMovieDb", "The Open Movie Database"],
                    "ImageFetchers": [
                        "TheMovieDb",
                        "The Open Movie Database",
                        "Embedded Image Extractor",
                        "Screen Grabber",
                    ],
                    "ImageFetcherOrder": [
                        "TheMovieDb",
                        "The Open Movie Database",
                        "Embedded Image Extractor",
                        "Screen Grabber",
                    ],
                },
                {
                    "Type": "Movie",
                    "MetadataFetchers": ["TheMovieDb", "The Open Movie Database"],
                    "MetadataFetcherOrder": ["TheMovieDb", "The Open Movie Database"],
                    "ImageFetchers": [
                        "TheMovieDb",
                        "The Open Movie Database",
                        "Embedded Image Extractor",
                        "Screen Grabber",
                    ],
                    "ImageFetcherOrder": [
                        "TheMovieDb",
                        "The Open Movie Database",
                        "Embedded Image Extractor",
                        "Screen Grabber",
                    ],
                },
            ],
            "LocalMetadataReaderOrder": ["Nfo"],
            "SubtitleDownloadLanguages": [],
            "DisabledSubtitleFetchers": [],
            "SubtitleFetcherOrder": [],
            "PathInfos": [{"Path": "/mnt/media"}],
        }
    }

    post(
        url="http://{}/Library/VirtualFolders?refreshLibrary=false&name=Library".format(
            JELLYFIN_HOST
        ),
        headers=headers,
        body=body,
    )


@step("jellyfin_setup_location_2")
def setup_location_2():
    logger.debug("For some reason we have to setup the location twice..")

    setup_location_logic()


@step("jellyfin_setup_remote_access")
def setup_remote_access():
    headers = {"Content-Type": "application/json"}
    logger.info("Setup the remote access")

    body = {"EnableRemoteAccess": True, "EnableAutomaticPortMapping": False}

    post(
        url="http://{}/Startup/RemoteAccess".format(JELLYFIN_HOST),
        headers=headers,
        body=body,
    )


@step("jellyfin_finalize")
def finalize():
    logger.info("Finalize the setup")

    post(url="http://{}/Startup/Complete".format(JELLYFIN_HOST), headers={}, body={})


setup_location_1()
setup_user()
setup_library()
setup_location_2()
setup_remote_access()
finalize()
