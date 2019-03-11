#  Drakkar-Software OctoBot
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
import json
import socket
import requests
import time
from launcher import OCTOBOT_DEFAULT_SERVER_PORT, CONFIG_CATEGORY_SERVICES, CONFIG_WEB, CONFIG_WEB_PORT, \
    OCTOBOT_CONFIG_FILE, OCTOBOT_API_MAX_RETRIES


class OctoBotConnector:

    def __init__(self):
        self.octobot_config = None
        self.port = OCTOBOT_DEFAULT_SERVER_PORT
        self.current_ip = socket.gethostbyname(socket.gethostname())
        self._get_current_octobot_address()

    def get_current_version(self, allow_retry=False):
        max_retries = OCTOBOT_API_MAX_RETRIES if allow_retry else 1
        for i in range(max_retries):
            try:
                return json.loads(requests.get(f"{self.get_web_interface_url()}/api/version").text).split(" ")[1]
            except Exception as e:
                if i < max_retries-1:
                    time.sleep(0.5)
                else:
                    raise e

    def get_web_interface_url(self):
        return f"http://{self.current_ip}:{self.port}"

    def is_alive(self):
        try:
            self.get_current_version()
            return True
        except Exception:
            return False

    def _get_current_octobot_address(self):
        if os.path.isfile(OCTOBOT_CONFIG_FILE):
            try:
                with open(OCTOBOT_CONFIG_FILE) as json_data_file:
                    self.octobot_config = json.load(json_data_file)
                if CONFIG_WEB in self.octobot_config[CONFIG_CATEGORY_SERVICES]:
                    if CONFIG_WEB_PORT in self.octobot_config[CONFIG_CATEGORY_SERVICES][CONFIG_WEB_PORT]:
                        self.port = self.octobot_config[CONFIG_CATEGORY_SERVICES][CONFIG_WEB_PORT]
            except Exception as e:
                print(f"Error when reading {OCTOBOT_CONFIG_FILE}: {e}")
