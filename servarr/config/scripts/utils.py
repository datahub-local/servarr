import json
import logging
import os
import functools
from json import JSONDecodeError
import requests

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

STATE_FILE_PATH = os.getenv("STATE_FILE_PATH", "/state/init_state.json")


def get_logger():
    return logger


def post(
    url: str,
    headers: dict = None,
    body: dict = None,
    session=None,
    method: str = "POST",
):
    """
    Handle POST requests towards an url, logging both
    the details before sending it and the response.

    Parameters
    ----------
    url : str
        HTTP request URL as string
    headers : dict
        HTTP headers to be used in the request
    body : dict
        Request body needed for the POST
    session : requests.Session
        Optional session to use for the request
    method : str
        Optional HTTP method to use (default is POST)
    """
    if headers is None:
        headers = {}

    logger.debug(
        " ".join(
            [
                "POST",
                url,
                ", ".join(f"{key}: {value}" for key, value in headers.items()),
                str(body),
            ]
        )
    )

    if session:
        response = session.request(method=method, url=url, json=body, headers=headers)
    else:
        response = requests.request(method=method, url=url, json=body, headers=headers)

    logger.debug(
        " ".join(
            ["Status Code:", str(response.status_code), "Response body:", response.text]
        )
    )

    response.raise_for_status()

    try:
        response_data = response.json()
    except JSONDecodeError:
        response_data = None

    return {"code": response.status_code, "response": response_data}


def get(url: str, headers: dict = None, session=None):
    """
    Handle GET requests towards an url, logging both
    the details before sending it and the response.

    Parameters
    ----------
    url : str
        HTTP request URL as string
    headers : dict
        HTTP headers to be used in the request
    session : requests.Session
        Optional session to use for the request
    """
    if headers is None:
        headers = {}

    logger.debug(
        " ".join(
            [
                "GET",
                url,
                ", ".join(f"{key}: {value}" for key, value in headers.items()),
            ]
        )
    )

    if session:
        response = session.get(url=url, headers=headers)
    else:
        response = requests.get(url=url, headers=headers)

    logger.debug(
        " ".join(
            ["Status Code:", str(response.status_code), "Response body:", response.text]
        )
    )

    response.raise_for_status()

    try:
        response_data = response.json()
    except JSONDecodeError:
        response_data = None

    return {"code": response.status_code, "response": response_data}


def load_state():
    if os.path.exists(STATE_FILE_PATH):
        try:
            with open(STATE_FILE_PATH, "r") as f:
                return json.load(f)
        except JSONDecodeError:
            return {}
    return {}


def save_state(state):
    with open(STATE_FILE_PATH, "w") as f:
        json.dump(state, f)


def is_step_completed(step_name):
    state = load_state()
    return state.get(step_name, False)


def mark_step_completed(step_name):
    state = load_state()
    state[step_name] = True
    save_state(state)


def step(step_name, exit_on_failure=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not is_step_completed(step_name):
                logger.info(f"Starting step: {step_name}")
                try:
                    result = func(*args, **kwargs)
                    mark_step_completed(step_name)
                    logger.info(f"Completed step: {step_name}")
                    return result
                except Exception as e:
                    logger.error(f"Error occurred in step {step_name}: {e}")
                    if exit_on_failure:
                        exit(1)
                    else:
                        raise e
            else:
                logger.info(f"Step already completed: {step_name}")

        return wrapper

    return decorator
