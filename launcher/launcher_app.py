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

from launcher import PROJECT_NAME, VERSION
from launcher import launcher_controller, OCTOBOT_NAME
from launcher.launcher_controller import Launcher, GITHUB_LATEST_BOT_RELEASE_URL, GITHUB_LATEST_LAUNCHER_RELEASE_URL
from launcher.web_app import WebApp


class LauncherApp(WebApp):
    PROGRESS_MIN = 0
    PROGRESS_MAX = 100

    def __init__(self):
        Launcher.ensure_minimum_environment()

        self.processing = False

        super().__init__()

    def create_components(self):
        # bot update
        pass

    def inc_progress(self, inc_size, to_min=False, to_max=False):
        # if to_max:
        #     self.progress["value"] = self.PROGRESS_MAX
        #     self.progress_label["text"] = f"{self.PROGRESS_MAX}%"
        # elif to_min:
        #     self.progress["value"] = self.PROGRESS_MIN
        #     self.progress_label["text"] = f"{self.PROGRESS_MIN}%"
        # else:
        #     self.progress["value"] += inc_size
        #     self.progress_label["text"] = f"{round(self.progress['value'], 1)}%"
        pass

    def update_bot_handler(self):
        if not self.processing:
            thread = Thread(target=self.update_bot, args=(self,))
            thread.start()

    def update_package_handler(self):
        if not self.processing:
            thread = Thread(target=self.update_package, args=(self,))
            thread.start()

    def update_launcher_handler(self):
        if not self.processing:
            # prevent binary to add self as first argument
            first_arg = sys.argv[0] if sys.argv[0].endswith(".py") else ""

            launcher_process = subprocess.Popen(
                [sys.executable, first_arg, "--update_launcher"] if first_arg else [sys.executable, "--update_launcher"]
            )

            if launcher_process:
                self.hide()
                launcher_process.wait()

                new_launcher_process = subprocess.Popen(
                    [sys.executable, first_arg] if first_arg else [sys.executable]
                )

                if new_launcher_process:
                    self.stop()

    def start_bot_handler(self, args=None):
        if not self.processing:
            bot_process = Launcher.execute_command_on_detached_bot(commands=args)

            if bot_process:
                self.hide()
                bot_process.wait()
                self.stop()

    def update_bot_version(self):
        current_server_bot_version = launcher_controller.Launcher.get_current_server_version(
            GITHUB_LATEST_BOT_RELEASE_URL)

        if Launcher.is_bot_package_installed():
            current_bot_version = self.update_bot_version_from_package()
        else:
            current_bot_version = self.update_bot_version_from_binary()

        # self.bot_version_label["text"] = f"Bot version : " \
        #     f"{current_bot_version if current_bot_version else 'Not found'}" \
        #     f" (Latest : " \
        #     f"{current_server_bot_version if current_server_bot_version else 'Not found'})"
        pass

    def update_bot_version_from_package(self):
        return pkg_resources.get_distribution(OCTOBOT_NAME).version

    def update_bot_version_from_binary(self):
        return launcher_controller.Launcher.get_current_bot_version()

    def update_launcher_version(self):
        current_server_launcher_version = launcher_controller.Launcher.get_current_server_version(
            GITHUB_LATEST_LAUNCHER_RELEASE_URL)
        # self.launcher_version_label["text"] = f"Launcher version : " \
        #     f"{VERSION} (Latest : " \
        #     f"{current_server_launcher_version if current_server_launcher_version else 'Not found'})"
        pass

    @staticmethod
    def update_bot(app=None):
        if app:
            app.processing = True
        launcher_controller.Launcher(app)
        if app:
            app.processing = False
            sleep(1)
            app.update_bot_version()

    @staticmethod
    def update_package(app=None):
        if app:
            app.processing = True
        launcher_controller.Launcher(app, force_package=True)
        if app:
            app.processing = False
            sleep(1)
            app.update_bot_version()

    @staticmethod
    def export_logs():
        # TODO
        pass

    @staticmethod
    def close_callback():
        os._exit(0)

    def start_app(self):
        self.start()

    def stop(self):
        self.stop()
