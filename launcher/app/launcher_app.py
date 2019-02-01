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

import launcher
from launcher.tools import environment
from launcher.app.web_app import WebApp
from launcher.tools.environment import ensure_minimum_environment
from launcher.tools.version import OctoBotVersion


class LauncherApp(WebApp):
    def __init__(self):
        ensure_minimum_environment()

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
            launcher.bot_instance = LauncherController.execute_command_on_detached_binary(OctoBotVersion().get_local_binary(),
                                                                                          commands=args)

            if launcher.bot_instance:
                launcher.bot_instance.wait()
                self.close()

    @staticmethod
    def update_bot(app=None):
        if app:
            app.processing = True
        environment.install_bot()
        if app:
            app.processing = False

    @staticmethod
    def update_package(app=None):
        if app:
            app.processing = True
        environment.install_bot(force_package=True)
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
