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

import os
import subprocess
import sys
from threading import Thread
from time import sleep

import pkg_resources

import launcher
from launcher import launcher_controller, OCTOBOT_NAME
from launcher.launcher_controller import Launcher, GITHUB_LATEST_BOT_RELEASE_URL, GITHUB_LATEST_LAUNCHER_RELEASE_URL
from launcher.web_app import WebApp


class LauncherApp(WebApp):
    def __init__(self):
        Launcher.ensure_minimum_environment()

        self.processing = False

        launcher.launcher_instance = self

        super().__init__()
        self.start_app()

    def update_bot_handler(self):
        if not self.processing:
            thread = Thread(target=self.update_bot, args=(self,))
            thread.start()

    def update_package_handler(self):
        if not self.processing:
            thread = Thread(target=self.update_package, args=(self,))
            thread.start()

    @staticmethod
    def launcher_start_args():
        # prevent binary to add self as first argument
        return sys.argv[0] if sys.argv[0].endswith(".py") else ""

    def update_launcher_handler(self):
        if not self.processing:
            launcher_process = subprocess.Popen(
                [sys.executable, self.launcher_start_args(), "--update_launcher"]
                if self.launcher_start_args() else [sys.executable, "--update_launcher"]
            )

            if launcher_process:
                launcher_process.wait()

                self.restart_launcher()

    def restart_launcher(self):
        self.prepare_stop()
        new_launcher_process = subprocess.Popen([sys.executable, self.launcher_start_args()]
                                                if self.launcher_start_args() else [sys.executable])

        if new_launcher_process:
            new_launcher_process.wait()
            self.stop()

    def start_bot_handler(self, args=None):
        if not self.processing:
            launcher.bot_instance = Launcher.execute_command_on_detached_bot(commands=args)

            if launcher.bot_instance:
                launcher.bot_instance.wait()
                self.close()

    def get_bot_server_version(self):
        return launcher_controller.Launcher.get_current_server_version(GITHUB_LATEST_BOT_RELEASE_URL)

    def get_launcher_server_version(self):
        return launcher_controller.Launcher.get_current_server_version(GITHUB_LATEST_LAUNCHER_RELEASE_URL)

    def get_bot_local_version(self):
        if Launcher.is_bot_package_installed():
            return self.get_bot_version_from_package()
        return self.get_bot_version_from_binary()

    def get_bot_version_from_package(self):
        return pkg_resources.get_distribution(OCTOBOT_NAME).version

    def get_bot_version_from_binary(self):
        return launcher_controller.Launcher.get_current_bot_version()

    @staticmethod
    def update_bot(app=None):
        if app:
            app.processing = True
        launcher_controller.Launcher(app)
        if app:
            app.processing = False

    @staticmethod
    def update_package(app=None):
        if app:
            app.processing = True
        launcher_controller.Launcher(app, force_package=True)
        if app:
            app.processing = False

    @staticmethod
    def export_logs():
        # TODO
        pass

    @staticmethod
    def close():
        os._exit(0)

    def start_app(self):
        self.start()
