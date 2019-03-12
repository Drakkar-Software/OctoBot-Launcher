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
import shutil
import sys
import zipfile
from urllib.request import urlretrieve

from past.translation import splitall

LAUNCHER_PATH = "launcher"
LAUNCHER_ENTRY_POINT = "entrypoint.py"
RELEASE_PATH = "updates"
LAUNCHER_SOURCE_EXT = "zip"
sys.path.append(os.path.dirname(sys.executable))


def get_latest_source_url():
    return "https://github.com/Drakkar-Software/OctoBot-Launcher/archive/master.zip"


def get_latest_release_source_file():
    return f"{LAUNCHER_PATH}.{LAUNCHER_SOURCE_EXT}"


def download_latest_release_sources():
    urlretrieve(get_latest_source_url(), get_latest_release_source_file())


def get_extraction_location():
    source_file = zipfile.ZipFile(get_latest_release_source_file(), 'r')
    return os.path.commonprefix(source_file.namelist())


def extraction_filter(members):
    for info in members:
        file_path = splitall(info.filename)
        if len(file_path) > 1 and file_path[1] in [LAUNCHER_PATH, LAUNCHER_ENTRY_POINT]:
            yield info


def extract_sources():
    if os.path.isfile(get_latest_release_source_file()):
        with zipfile.ZipFile(get_latest_release_source_file()) as source_zip:
            source_zip.extractall(members=extraction_filter(source_zip.infolist()), path=RELEASE_PATH)


def move_sources():
    try:
        shutil.rmtree(LAUNCHER_PATH)
    except FileNotFoundError:
        pass

    try:
        shutil.move(os.path.join(RELEASE_PATH, get_extraction_location(), LAUNCHER_PATH), os.getcwd())
        shutil.move(os.path.join(RELEASE_PATH, get_extraction_location(), LAUNCHER_ENTRY_POINT), os.getcwd())
    except FileNotFoundError:
        logging.warning("Can't move updated sources.")


def update_launcher():
    download_latest_release_sources()
    extract_sources()
    move_sources()
    logging.info("Launcher updated")


def main():
    logging.getLogger().setLevel(logging.INFO)

    if not os.path.exists(LAUNCHER_PATH):
        update_launcher()
        logging.info("Launcher fresh install...")

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
