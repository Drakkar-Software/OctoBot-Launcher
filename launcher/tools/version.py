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
import glob
import logging
import os
import subprocess
import sys
from distutils.version import LooseVersion
from subprocess import PIPE

import pkg_resources

from launcher import LINUX_OS_NAME, FORCE_BINARY, \
    WINDOWS_OS_NAME, MAC_OS_NAME, PROJECT_NAME, OCTOBOT_NAME, launcher_instance, inc_progress
from launcher.tools import executor, BINARY_DOWNLOAD_PROGRESS_SIZE


class Version:
    PROJECT = ""
    NOT_INSTALLED_VERSION = "not installed"

    def is_package_installed(self):
        try:
            pkg_resources.get_distribution(self.PROJECT)
            return True
        except (pkg_resources.DistributionNotFound, pkg_resources.RequirementParseError):
            return False

    def download_package(self):
        try:
            cmd = [sys.executable, "-m", "pip", "install", "-U", self.PROJECT]
            return subprocess.Popen(cmd, stdout=PIPE).stdout.read().rstrip().decode()
        except PermissionError as e:
            logging.error(f"Failed to update package : {e}")
        except FileNotFoundError as e:
            logging.error(f"Can't find a valid python executable : {e}")

    def get_local_binary(self, force_binary=False):
        binary = None

        if not force_binary and self.is_package_installed():
            binary = self.PROJECT
        else:
            try:
                # try to found in current folder binary
                if os.name == LINUX_OS_NAME:
                    binary = f"./{next(iter(glob.glob(f'{self.PROJECT}*')))}"

                elif os.name == WINDOWS_OS_NAME:
                    binary = next(iter(glob.glob(f'{self.PROJECT}*.exe')))

                elif os.name == MAC_OS_NAME:
                    binary = f"./{next(iter(glob.glob(f'{self.PROJECT}*')))}"
            except StopIteration:
                binary = None

        return binary

    @staticmethod
    def is_binary_available(binary_path):
        if binary_path is None or not os.path.isfile(binary_path):
            return False
        return True

    def get_current_version(self, binary_path=None, force_binary=FORCE_BINARY):
        if not binary_path:
            binary_path = self.get_local_binary(force_binary=force_binary)
        if not self.is_binary_available(binary_path):
            return self.NOT_INSTALLED_VERSION
        return executor.execute_command_on_current_binary(binary_path, ["--version"]).split("\r\n")[0]

    def get_local_version_or_download(self, github_instance, binary_path,
                                      latest_release_data=None, force_binary=FORCE_BINARY):
        last_release_version = github_instance.get_current_server_version(latest_release_data=latest_release_data)
        current_version = self.get_current_version(binary_path, force_binary=force_binary)

        try:
            if current_version == self.NOT_INSTALLED_VERSION:
                check_new_version = True
            else:
                check_new_version = LooseVersion(current_version) < LooseVersion(last_release_version)
        except AttributeError:
            check_new_version = False

        if check_new_version:
            logging.info(f"Upgrading {self.PROJECT} : from {current_version} to {last_release_version}...")
            return github_instance.download_binary(replace=True)
        else:
            logging.info(f"Nothing to do : {self.PROJECT} is up to date")
            if launcher_instance:
                inc_progress(BINARY_DOWNLOAD_PROGRESS_SIZE)
            return binary_path


class OctoBotVersion(Version):
    PROJECT = OCTOBOT_NAME


class LauncherVersion(Version):
    PROJECT = PROJECT_NAME
