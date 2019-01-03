import argparse
import importlib
import logging

from launcher.launcher import update_launcher, start_launcher

if __name__ == '__main__':
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

    args = parser.parse_args()

    update_launcher()

    try:
        from launcher.launcher_app import *
    except ImportError:
        importlib.import_module("launcher.launcher_app")

    start_launcher(args)
