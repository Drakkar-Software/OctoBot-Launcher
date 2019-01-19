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

PROJECT_NAME = "OctoBot-Launcher"
OCTOBOT_NAME = "OctoBot"
SHORT_VERSION = "1.1.1"
PATCH_VERSION = ""  # patch : pX
VERSION_DEV_PHASE = ""  # alpha : a / beta : b / release candidate : rc
VERSION_PHASE = ""  # XX
VERSION = f"{SHORT_VERSION}{VERSION_DEV_PHASE}{VERSION_PHASE}"
LONG_VERSION = f"{SHORT_VERSION}{PATCH_VERSION}{VERSION_DEV_PHASE}{VERSION_PHASE}"

OCTOBOT_VERSION_RELEASE_PHASE = "beta"
OCTOBOT_LAUNCHER_VERSION_BRANCH = "master"

DEFAULT_CONFIG_FILE = "config/default_config.json"
LOGGING_CONFIG_FILE = "config/logging_config.ini"

GITHUB_RAW_CONTENT_URL = "https://raw.githubusercontent.com"
GITHUB_API_CONTENT_URL = "https://api.github.com"
GITHUB_BASE_URL = "https://github.com"
GITHUB_ORGANISATION = "Drakkar-Software"
OCTOBOT_GITHUB_REPOSITORY = f"{GITHUB_ORGANISATION}/{OCTOBOT_NAME}"
LAUNCHER_GITHUB_REPOSITORY = f"{GITHUB_ORGANISATION}/{PROJECT_NAME}"
GITHUB_URL = f"{GITHUB_BASE_URL}/{OCTOBOT_GITHUB_REPOSITORY}"

LAUNCHER_PATH = "launcher"

CONFIG_FILE = "config.json"

REPOSITORY_BRANCH = "master"

TENTACLES_PATH = "tentacles"
CONFIG_DEFAULT_EVALUATOR_FILE = "config/default_evaluator_config.json"
CONFIG_DEFAULT_TRADING_FILE = "config/default_trading_config.json"

CONFIG_INTERFACES = "interfaces"
CONFIG_INTERFACES_WEB = "web"

OCTOBOT_BACKGROUND_IMAGE = "static/img/octobot.png"
OCTOBOT_ICON = "static/favicon.ico"


class DeliveryPlatformsName(Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    MAC = "osx"
