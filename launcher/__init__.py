#  Drakkar-Software OctoBot-Launcher
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
from enum import Enum

import flask

PROJECT_NAME = "OctoBot-Launcher"
OCTOBOT_BINARY = "OctoBot-Binary"
OCTOBOT_NAME = "OctoBot"
SHORT_VERSION = "2.0.3"
PATCH_VERSION = ""  # patch : pX
VERSION_DEV_PHASE = ""  # alpha : a / beta : b / release candidate : rc
VERSION_PHASE = ""  # XX
VERSION = f"{SHORT_VERSION}{VERSION_DEV_PHASE}{VERSION_PHASE}"
LONG_VERSION = f"{SHORT_VERSION}{PATCH_VERSION}{VERSION_DEV_PHASE}{VERSION_PHASE}"

FORCE_BINARY = True
REDUCE_GITHUB_REQUESTS = False

OCTOBOT_REFERENCE_BRANCH = "master"
OCTOBOT_LAUNCHER_VERSION_BRANCH = "master"
OCTOBOT_DEV_PHASE = "beta"

DEFAULT_CONFIG_FILE = "config/default_config.json"
LOGGING_CONFIG_FILE = "config/logging_config.ini"

GITHUB_RAW_CONTENT_URL = "https://raw.githubusercontent.com"
GITHUB_API_CONTENT_URL = "https://api.github.com"
GITHUB_BASE_URL = "https://github.com"
GITHUB_ORGANISATION = "Drakkar-Software"
OCTOBOT_GITHUB_REPOSITORY = f"{GITHUB_ORGANISATION}/{OCTOBOT_NAME}"
OCTOBOT_BINARY_GITHUB_REPOSITORY = f"{GITHUB_ORGANISATION}/{OCTOBOT_BINARY}"
LAUNCHER_GITHUB_REPOSITORY = f"{GITHUB_ORGANISATION}/{PROJECT_NAME}"
GITHUB_URL = f"{GITHUB_BASE_URL}/{OCTOBOT_GITHUB_REPOSITORY}"

LAUNCHER_PATH = "launcher"

CONFIG_FILE = "config.json"
CONFIG_FILE_SCHEMA_NAME = "config_schema.json"

REPOSITORY_BRANCH = "master"

TENTACLES_PATH = "tentacles"
CONFIG_FILE_SCHEMA_WITH_PATH = f"config/{CONFIG_FILE_SCHEMA_NAME}"
CONFIG_DEFAULT_EVALUATOR_FILE = "config/default_evaluator_config.json"
CONFIG_DEFAULT_TRADING_FILE = "config/default_trading_config.json"

CONFIG_INTERFACES = "interfaces"
CONFIG_INTERFACES_WEB = "web"

OCTOBOT_CONFIG_FILE = "config.json"
CONFIG_CATEGORY_SERVICES = "services"
CONFIG_WEB = "web"
CONFIG_WEB_PORT = "port"

OCTOBOT_BACKGROUND_IMAGE = "static/img/octobot.png"
OCTOBOT_ICON = "static/favicon.ico"

DEFAULT_SERVER_IP = '0.0.0.0'
DEFAULT_SERVER_PORT = 5010  # prevent conflicts with OctoBot web interface

OCTOBOT_DEFAULT_SERVER_PORT = 5001
OCTOBOT_API_MAX_RETRIES = 20

server_instance = flask.Flask(__name__)
launcher_instance = None
bot_instance = None
processing = 0

WINDOWS_OS_NAME = "nt"
MAC_OS_NAME = "mac"
LINUX_OS_NAME = "posix"


class DeliveryPlatformsName(Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    MAC = "osx"


def get_launcher_instance():
    global launcher_instance
    return launcher_instance


def inc_progress(inc_size, to_min=False, to_max=False):
    global processing
    if to_max:
        processing = 100
    elif to_min:
        processing = 0
    else:
        processing += inc_size


def load_routes():
    from launcher.app import app_controller
