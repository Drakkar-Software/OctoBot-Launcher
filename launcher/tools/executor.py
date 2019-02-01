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


import logging
import subprocess
from subprocess import PIPE


def execute_command_on_current_binary(binary_path, commands):
    try:
        cmd = [f"{binary_path}"] + commands
        return subprocess.Popen(cmd, stdout=PIPE).stdout.read().rstrip().decode()
    except PermissionError as e:
        logging.error(f"Failed to run bot with command {commands} : {e}")
    except FileNotFoundError as e:
        logging.error(f"Can't find a valid binary")


def execute_command_on_detached_binary(binary_path, commands=None):
    try:
        cmd = [f"{binary_path}"] + (commands if commands else [])
        return subprocess.Popen(cmd)
    except Exception as e:
        logging.error(f"Failed to run detached bot with command {commands} : {e}")
        return None
