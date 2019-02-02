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
import importlib
import logging
import os
import sys

import requests

LAUNCHER_PATH = "launcher"
LAUNCHER_URL = f"https://raw.githubusercontent.com/Drakkar-Software/OctoBot-Launcher/master/{LAUNCHER_PATH}"

sys.path.append(os.path.dirname(sys.executable))


def update_launcher(force=False):
    for file in []:
        create_launcher_files(f"{LAUNCHER_URL}/{file}", f"{LAUNCHER_PATH}/{file}", force=force)
    logging.info("Launcher updated")


def create_launcher_files(file_to_dl, result_file_path, force=False):
    file_content = requests.get(file_to_dl).text
    directory = os.path.dirname(result_file_path)

    if not os.path.exists(directory) and directory:
        os.makedirs(directory)

    file_name = result_file_path
    if (not os.path.isfile(file_name) and file_name) or force:
        with open(file_name, "w") as new_file_from_dl:
            new_file_from_dl.write(file_content)


def main():
    logging.getLogger().setLevel(logging.INFO)

    update_launcher()

    try:
        from launcher.launcher_entry import launcher
    except ImportError:
        importlib.import_module("launcher.app.launcher_app")

    try:
        launcher()
    except NameError as e:
        logging.error(f"Can't start launcher, please try to reinstall.\n{e}")


if __name__ == '__main__':
    main()
