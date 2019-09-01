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
import logging
import os
import subprocess

import urllib.request

from launcher import CONFIG_FILE, OCTOBOT_GITHUB_REPOSITORY, \
    GITHUB_RAW_CONTENT_URL, OCTOBOT_REFERENCE_BRANCH, DEFAULT_CONFIG_FILE, LOGGING_CONFIG_FILE, \
    CONFIG_DEFAULT_EVALUATOR_FILE, CONFIG_DEFAULT_TRADING_FILE, OCTOBOT_NAME, LINUX_OS_NAME, MAC_OS_NAME, \
    TENTACLES_PATH, inc_progress, FORCE_BINARY, CONFIG_FILE_SCHEMA_WITH_PATH, STRATEGY_OPTIMIZER_DATA_FOLDER
from launcher.tools import executor
from launcher.tools.github import GithubOctoBot
from launcher.tools.version import OctoBotVersion

FOLDERS_TO_CREATE = ["logs", "backtesting/collector/data", STRATEGY_OPTIMIZER_DATA_FOLDER]
STRATEGY_OPTIMIZER_DATA = [
    "binance_ADA_BTC_20180722_223335.data",
    "binance_BTC_USDT_20180428_121156.data",
    "binance_ETH_USDT_20180716_131148.data",
    "binance_ICX_BTC_20180716_131148.data",
    "binance_NEO_BTC_20180716_131148.data",
    "binance_ONT_BTC_20180722_230900.data",
    "binance_POWR_BTC_20180722_234855.data",
    "binance_VEN_BTC_20180716_131148.data",
    "binance_XLM_BTC_20180722_234305.data",
    "binance_XRB_BTC_20180716_131148.data",
    "bittrex_ADA_BTC_20180722_223357.data",
    "bittrex_ETC_BTC_20180726_210341.data",
    "bittrex_NEO_BTC_20180722_195942.data",
    "bittrex_WAX_BTC_20180726_205032.data",
    "bittrex_XRP_BTC_20180726_210927.data",
    "bittrex_XVG_BTC_20180726_211225.data"
]

INSTALL_DOWNLOAD = [
    (
        f"{GITHUB_RAW_CONTENT_URL}/cjhutto/vaderSentiment/master/vaderSentiment/emoji_utf8_lexicon.txt",
        "vaderSentiment/emoji_utf8_lexicon.txt"),
    (
        f"{GITHUB_RAW_CONTENT_URL}/cjhutto/vaderSentiment/master/vaderSentiment/vader_lexicon.txt",
        "vaderSentiment/vader_lexicon.txt"),
]

OCTOBOT_REPOSITORY_FILES_ROOT = f"{GITHUB_RAW_CONTENT_URL}/{OCTOBOT_GITHUB_REPOSITORY}/{OCTOBOT_REFERENCE_BRANCH}"

INSTALL_DOWNLOAD += [(f"{OCTOBOT_REPOSITORY_FILES_ROOT}/{STRATEGY_OPTIMIZER_DATA_FOLDER}/{data_file}",
                      f"{STRATEGY_OPTIMIZER_DATA_FOLDER}/{data_file}")
                     for data_file in STRATEGY_OPTIMIZER_DATA]

FILES_TO_DOWNLOAD = [
    (
        f"{OCTOBOT_REPOSITORY_FILES_ROOT}/{DEFAULT_CONFIG_FILE}", CONFIG_FILE
    ),
    (
        f"{OCTOBOT_REPOSITORY_FILES_ROOT}/{DEFAULT_CONFIG_FILE}", DEFAULT_CONFIG_FILE
    ),
    (
        f"{OCTOBOT_REPOSITORY_FILES_ROOT}/{CONFIG_FILE_SCHEMA_WITH_PATH}", CONFIG_FILE_SCHEMA_WITH_PATH
    ),
    (
        f"{OCTOBOT_REPOSITORY_FILES_ROOT}/{CONFIG_DEFAULT_EVALUATOR_FILE}", CONFIG_DEFAULT_EVALUATOR_FILE
    ),
    (
        f"{OCTOBOT_REPOSITORY_FILES_ROOT}/{CONFIG_DEFAULT_TRADING_FILE}", CONFIG_DEFAULT_TRADING_FILE
    ),
    (
        f"{OCTOBOT_REPOSITORY_FILES_ROOT}/{LOGGING_CONFIG_FILE}", LOGGING_CONFIG_FILE
    )
]

LIB_FILES_DOWNLOAD_PROGRESS_SIZE = 5
CREATE_FOLDERS_PROGRESS_SIZE = 5


def create_environment():
    inc_progress(0, to_min=True)
    logging.info(f"{OCTOBOT_NAME} is checking your environment...")

    inc_progress(1)
    ensure_file_environment(INSTALL_DOWNLOAD)

    inc_progress(LIB_FILES_DOWNLOAD_PROGRESS_SIZE - 1)
    inc_progress(CREATE_FOLDERS_PROGRESS_SIZE)

    logging.info(f"Your {OCTOBOT_NAME} environment is ready !")


def install_bot(force_package=False):
    create_environment()

    binary_path = GithubOctoBot().update_binary(OctoBotVersion(), force_package=force_package,
                                                force_binary=FORCE_BINARY)

    # give binary execution rights if necessary
    if binary_path:
        binary_execution_rights(binary_path)

    # if update tentacles
    if binary_path:
        executable_path = OctoBotVersion().get_local_binary(force_binary=FORCE_BINARY)
        update_tentacles(executable_path, force_install=True)
    else:
        logging.error(f"No {OCTOBOT_NAME} found to update tentacles.")


def _ensure_directory(file_path):
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory) and directory:
        os.makedirs(directory)


def ensure_minimum_environment():
    try:
        for folder in FOLDERS_TO_CREATE:
            if not os.path.exists(folder) and folder:
                os.makedirs(folder)

        ensure_file_environment(FILES_TO_DOWNLOAD)
    except Exception as e:
        print(f"Error when creating minimum launcher environment: {e} this should not prevent launcher "
              f"from working.")


def ensure_file_environment(file_to_download):
    # download files
    for file_to_dl in file_to_download:

        _ensure_directory(file_to_dl[1])

        file_name = file_to_dl[1]
        if not os.path.isfile(file_name) and file_name:
            urllib.request.urlretrieve(file_to_dl[0], file_name)


def update_tentacles(binary_path, force_install=False):
    if binary_path:
        # update tentacles if installed
        if not force_install and os.path.exists(TENTACLES_PATH):
            executor.execute_command_on_current_binary(binary_path, ["-p", "update", "all"])
            logging.info(f"Tentacles : all default tentacles have been updated.")
        else:
            executor.execute_command_on_current_binary(binary_path, ["-p", "install", "all", "force"])
            logging.info(f"Tentacles : all default tentacles have been installed.")


def binary_execution_rights(binary_path):
    if os.name in [LINUX_OS_NAME, MAC_OS_NAME]:
        try:
            rights_process = subprocess.Popen(["chmod", "+x", binary_path])
        except Exception as e:
            logging.error(f"Failed to give execution rights to {binary_path} : {e}")
            rights_process = None

        if not rights_process:
            # show message if user has to type the command
            message = f"{OCTOBOT_NAME} binary need execution rights, " \
                f"please type in a command line 'sudo chmod +x ./{OCTOBOT_NAME}'"
            logging.warning(message)
            # if self.launcher_app:
            #     self.launcher_app.show_alert(f"{message} and then press OK", bitmap=WARNING)
