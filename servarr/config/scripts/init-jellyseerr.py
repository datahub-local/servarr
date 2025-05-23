#!/usr/local/bin/python3

import logging
import os
from json import JSONDecodeError

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

API_KEY = os.getenv("API_KEY")
JELLYFIN_USERNAME = os.getenv("JELLYFIN_USERNAME")
JELLYFIN_PASSWORD = os.getenv("JELLYFIN_PASSWORD")
JELLYFIN_EMAIL = os.getenv("JELLYFIN_EMAIL")
JELLYSEERR_HOST = os.getenv("JELLYSEERR_HOST")
JELLYSEERR_PORT = os.getenv("JELLYSEERR_PORT")
JELLYFIN_HOST = os.getenv("JELLYFIN_HOST")
JELLYFIN_PORT = os.getenv("JELLYFIN_PORT")
SONARR_HOST = os.getenv("SONARR_HOST")
SONARR_PORT = int(os.getenv("SONARR_PORT", "8989"))
SONARR_EXTERNAL_URL = os.getenv("SONARR_EXTERNAL_URL")
RADARR_HOST = os.getenv("RADARR_HOST")
RADARR_PORT = int(os.getenv("RADARR_PORT", "7878"))
RADARR_EXTERNAL_URL = os.getenv("RADARR_EXTERNAL_URL")

jellyseer_url = "http://{0}:{1}".format(JELLYSEERR_HOST, JELLYSEERR_PORT)

session = requests.Session()

def make_get(endpoint=""):

    url = "{0}{1}".format(jellyseer_url, endpoint)

    logger.debug(" ".join([
        url,
        "GET",
        ", ".join([f'{key}: {value}' for key,value in session.headers.items()]),
        ", ".join([f'{key}: {value}' for key,value in session.cookies.items()])
    ]))

    response = session.get(
        url=url,
        verify=False,
    )

    logger.debug(" ".join([
        "Status Code:",
        str(response.status_code),
        "Response body:",
        response.text
    ]))

    response.raise_for_status()
    try:
        return response.json()
    except JSONDecodeError:
        return response.text

def make_post(endpoint="", body=None):

    url = "{0}{1}".format(jellyseer_url, endpoint)

    logger.debug(" ".join([
        url,
        "POST",
        "Body:",
        str(body),
        ", ".join([f'{key}: {value}' for key,value in session.headers.items()]),
        ", ".join([f'{key}: {value}' for key,value in session.cookies.items()])
    ]))

    response = session.post(
        url=url,
        json=body,
        verify=False,
    )

    logger.debug(" ".join([
        "Status Code:",
        str(response.status_code),
        "Response body:",
        response.text
    ]))

    response.raise_for_status()
    try:
        return response.json()
    except JSONDecodeError:
        return response.text

logger.info("Initizalizing JellySeer")

########## JELLYFIN INTEGRATION

logger.info("Integrating Jellyfin")

jellyfin_endpoint = "/api/v1/auth/jellyfin"

jellyfin_body = {
  "username": JELLYFIN_USERNAME,
  "email": JELLYFIN_EMAIL,
  "password": JELLYFIN_PASSWORD,
  "hostname": JELLYFIN_HOST,
  "port": int(JELLYFIN_PORT),
  "useSsl": False,
  "urlBase": "",
  "serverType":2
}

jellyfin_response = make_post(jellyfin_endpoint, body=jellyfin_body)

logger.debug("Fetching info from response..")
token = jellyfin_response["jellyfinAuthToken"]
device_id = jellyfin_response["jellyfinDeviceId"]

logger.debug("Device ID: {0}. Jellyfin Token: {1}".format(device_id, token))

######### AUTH

#print("")
#print("Getting API Key")
#print("")

#settings_endpoint="/settings/main"

#settings_response = make_get(settings_endpoint)

#apikey=settings_response['apiKey']

#headers={ 'X-Api-Key': apikey }
#print("API KEY OBTAINED: {0}.".format(apikey))

############ SONARR

logger.info("Integrating Sonarr")

sonarr_endpoint = "/api/v1/settings/sonarr"
sonarr_body = {
    "name": "Sonarr",
    "hostname": SONARR_HOST,
    "port": 8989,
    "apiKey": API_KEY,
    "useSsl": False,
    "activeProfileId": 4,
    "activeLanguageProfileId": 1,
    "activeProfileName": "HD-1080p",
    "activeDirectory": "/mnt/media",
    "activeAnimeProfileId": 4,
    "activeAnimeLanguageProfileId": 1,
    "activeAnimeProfileName": "HD-1080p",
    "activeAnimeDirectory": "/mnt/media",
    "tags": [],
    "animeTags": [],
    "is4k": False,
    "isDefault": True,
    "enableSeasonFolders": True,
    "syncEnabled": False,
    "preventSearch": False,
    "tagRequests": True,
}

if SONARR_EXTERNAL_URL:
    sonarr_body["externalUrl"] = SONARR_EXTERNAL_URL

sonarr_response = make_post(sonarr_endpoint, body=sonarr_body)

############ RADARR

logger.info("Integrating Radarr")

radarr_endpoint = "/api/v1/settings/radarr"
radarr_body = {
    "name": "Radarr",
    "hostname": RADARR_HOST,
    "port": RADARR_PORT,
    "apiKey": API_KEY,
    "useSsl": False,
    "activeProfileId": 4,
    "activeProfileName": "HD-1080p",
    "activeDirectory": "/mnt/media",
    "is4k": False,
    "minimumAvailability": "released",
    "tags": [],
    "isDefault": True,
    "syncEnabled": False,
    "preventSearch": False,
    "tagRequests": True,
}

if RADARR_EXTERNAL_URL:
    radarr_body["externalUrl"] = RADARR_EXTERNAL_URL


radarr_response = make_post(radarr_endpoint, body=radarr_body)


############ FINALIZE

logger.info("Finalization phase")

finalize_endpoint = "/api/v1/settings/initialize"
finalize_body = {}

finalize_response = make_post(finalize_endpoint, body=finalize_body)

enable_telegram = os.getenv("TELEGRAM_NOTIFICATION_ENABLED", 'False').lower() in ('true', '1', 't')
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
telegram_apitoken = os.getenv("TELEGRAM_BOT_APITOKEN")

if enable_telegram:
    telegram_endpoint = "/api/v1/settings/notifications/telegram"
    telegram_body = {"enabled":True,"types":4062,"options":{}}
    telegram_body['options']= {"botAPI":telegram_apitoken,"chatId":telegram_chat_id,"sendSilently":False}

    telegram_response = make_post(telegram_endpoint, body=telegram_body)

external_auth_enabled = os.getenv("JELLYSEERR__AUTH__METHOD", '').lower() in ('external')

if external_auth_enabled:
    network_endpoint = "/api/v1/settings/network"
    network_body = {"trustProxy":True}

    network_response = make_post(network_endpoint, body=network_body)


