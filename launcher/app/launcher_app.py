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
import signal
import subprocess
import sys
from threading import Thread

import launcher
from entrypoint import update_launcher
from launcher.tools import environment, executor
from launcher.app.web_app import WebApp
from launcher.tools.version import OctoBotVersion


class LauncherApp(WebApp):
    def __init__(self):
        launcher.launcher_instance = self

        super().__init__()
        self.start_app()

    def update_bot_handler(self):
        thread = Thread(target=self.update_bot, args=(self,))
        thread.start()

    def update_package_handler(self):
        thread = Thread(target=self.update_bot, args=(self,))
        thread.start()

    @staticmethod
    def launcher_start_args():
        # prevent binary to add self as first argument
        return sys.argv[0] if sys.argv[0].endswith(".py") else ""

    def update_launcher_handler(self):
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

    def stop_launcher(self):
        self.prepare_stop()
        self.stop()

    @staticmethod
    def start_bot_handler(args=None):
        launcher.bot_instance = executor.execute_command_on_detached_binary(OctoBotVersion().get_local_binary(),
                                                                            commands=args)
        # if launcher.bot_instance:
        #     launcher.bot_instance.wait()

    @staticmethod
    def is_bot_alive():
        return launcher.bot_instance is not None and launcher.bot_instance.poll() is None

    @staticmethod
    def stop_bot():
        if launcher.bot_instance:
            os.kill(launcher.bot_instance.pid, signal.SIGINT)
            launcher.bot_instance.terminate()
            launcher.bot_instance = None

    @staticmethod
    def update_bot(force_package=False):
        environment.install_bot(force_package=force_package)

    @staticmethod
    def update_launcher():
        update_launcher()

    def export_logs(self):
        # TODO
        pass

    @staticmethod
    def close():
        os._exit(0)

    def start_app(self):
        self.start()
