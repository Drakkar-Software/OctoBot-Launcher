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

import argparse
import importlib
import logging
import sys

from launcher.launcher import update_launcher, start_launcher


def main(args=sys.argv[1:]):
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='OctoBot - Launcher')
    parser.add_argument('-v', '--version', help='show OctoBot Launcher current version',
                        action='store_true')
    parser.add_argument('-u', '--update', help='update OctoBot with the latest version available',
                        action='store_true')
    parser.add_argument('-l', '--update_launcher', help='update OctoBot Launcher with the latest version available',
                        action='store_true')
    parser.add_argument('-e', '--export_logs', help="export Octobot's last logs",
                        action='store_true')
    parser.add_argument('-ng', '--no_gui', help="Without gui",
                        action='store_true')

    args = parser.parse_args(args)

    update_launcher()

    try:
        import launcher.launcher_app
    except ImportError:
        importlib.import_module("launcher.launcher_app")

    if not args.no_gui:
        start_launcher(args)


if __name__ == '__main__':
    main()
