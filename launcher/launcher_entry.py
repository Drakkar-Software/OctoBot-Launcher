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
import logging
import sys
import webbrowser

from launcher import VERSION
from launcher.tools import environment
from launcher.tools.environment import ensure_minimum_environment


def launcher(args=sys.argv[1:]):
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='OctoBot - Launcher')
    parser.add_argument('-e', '--export_logs', help="export Octobot's last logs",
                        action='store_true')
    parser.add_argument('-v', '--version', help='show OctoBot Launcher current version',
                        action='store_true')
    parser.add_argument('-u', '--update', help='update OctoBot with the latest version available',
                        action='store_true')
    parser.add_argument('-s', '--start', help='Start OctoBot. OctoBot starting options can be added after '
                                              '-s or --start. Examples: "-s no t" will start OctoBot '
                                              'with "ng" option and "t" that will use telegram interface, without gui.',
                        nargs='*')
    parser.add_argument('-nw', '--no_web', help="Without web server", action='store_true')

    args = parser.parse_args(args)

    start_launcher(args)


def start_launcher(args):
    if args.version:
        print(VERSION)
    else:
        ensure_minimum_environment()
        from launcher.app.launcher_app import LauncherApp
        if not args.no_web:
            try:
                app = LauncherApp()
                webbrowser.open(app.get_web_server_url())
            except Exception as e:
                logging.error(f"Can't start gui, please try command line interface (use --help).\n{e}")

        if args.update:
            environment.install_bot(force_package=False)
        elif args.start:
            LauncherApp().start_bot_handler([f"-{arg}" for arg in args.start] if args.start else None)
        elif args.export_logs:
            pass
        else:
            pass
