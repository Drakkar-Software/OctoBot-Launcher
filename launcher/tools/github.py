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
import json
import logging
import os

import requests

from launcher import GITHUB_API_CONTENT_URL, LAUNCHER_GITHUB_REPOSITORY, \
    OCTOBOT_BINARY_GITHUB_REPOSITORY, WINDOWS_OS_NAME, DeliveryPlatformsName, LINUX_OS_NAME, OCTOBOT_NAME, PROJECT_NAME, \
    inc_progress, OCTOBOT_DEV_PHASE
from launcher.tools import BINARY_DOWNLOAD_PROGRESS_SIZE


class Github:
    PROJECT_REPOSITORY = ""
    PROJECT = ""

    def get_latest_release_url(self):
        return f"{GITHUB_API_CONTENT_URL}/repos/{self.PROJECT_REPOSITORY}/releases/latest"

    def get_latest_release_data(self):
        return json.loads(requests.get(self.get_latest_release_url()).text)

    def get_asset_from_release_data(self):
        latest_release_data = self.get_latest_release_data()
        os_name = None

        # windows
        if os.name == WINDOWS_OS_NAME:
            os_name = DeliveryPlatformsName.WINDOWS

        # linux
        if os.name == LINUX_OS_NAME:
            os_name = DeliveryPlatformsName.LINUX

        # mac
        if os.name == 'mac':
            os_name = DeliveryPlatformsName.MAC

        # search for corresponding release
        try:
            for asset in latest_release_data["assets"]:
                asset_name, _ = os.path.splitext(asset["name"])
                if f"{self.PROJECT}_{os_name.value}" in asset_name:
                    return asset
        except KeyError as e:
            logging.error(f"Can't find any asset : {e}")
        return None

    def get_current_server_version(self, latest_release_data=None):
        if not latest_release_data:
            latest_release_data = self.get_latest_release_data()
        try:
            tag_name = latest_release_data["tag_name"]
            dev_phase_tag = f"-{OCTOBOT_DEV_PHASE}"
            if dev_phase_tag in tag_name:
                return tag_name.split(dev_phase_tag)[0]
            else:
                return tag_name
        except KeyError:
            return None

    def download_binary(self, replace=False):
        binary = self.get_asset_from_release_data()

        if binary:
            final_size = binary["size"]
            increment = (BINARY_DOWNLOAD_PROGRESS_SIZE / (final_size / 1024))

            r = requests.get(binary["browser_download_url"], stream=True)

            binary_name, binary_ext = os.path.splitext(binary["name"])
            path = f"{self.PROJECT}{binary_ext}"

            if r.status_code == 200:

                if replace and os.path.isfile(path):
                    try:
                        os.remove(path)
                    except OSError as e:
                        logging.error(f"Can't remove old version binary : {e}")

                with open(path, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                        inc_progress(increment)

            return path
        else:
            logging.error("Release not found on server")
            return None

    def update_binary(self, version_instance, force_package=False, force_binary=False):
        # parse latest release
        try:
            logging.info(f"{self.PROJECT} is checking for updates...")
            latest_release_data = self.get_latest_release_data()

            # try to find binary / package
            binary_path = version_instance.get_local_binary()

            if (version_instance.is_package_installed() and not force_binary) or force_package:
                version_instance.download_package()
                return binary_path
            else:
                # try to find in current folder binary
                # if current octobot binary found
                if binary_path:
                    logging.info(f"{self.PROJECT} installation found, analyzing...")
                    return version_instance.get_local_version_or_download(self, binary_path, latest_release_data)
                else:
                    return self.download_binary(latest_release_data)
        except Exception as e:
            logging.exception(f"Failed to download latest release data : {e}")


class GithubOctoBot(Github):
    PROJECT_REPOSITORY = OCTOBOT_BINARY_GITHUB_REPOSITORY
    PROJECT = OCTOBOT_NAME


class GithubLauncher(Github):
    PROJECT_REPOSITORY = LAUNCHER_GITHUB_REPOSITORY
    PROJECT = PROJECT_NAME
