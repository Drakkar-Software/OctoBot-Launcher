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
import threading
import socket

from werkzeug.serving import make_server

from launcher import DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT, load_routes, server_instance


class WebApp(threading.Thread):
    def __init__(self, web_ip=DEFAULT_SERVER_IP, web_port=DEFAULT_SERVER_PORT):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        self.server_ip = web_ip
        self.server_port = web_port

        self.srv = make_server(host=self.server_ip,
                               port=self.server_port,
                               threaded=True,
                               app=server_instance)
        self.ctx = server_instance.app_context()
        self.ctx.push()

        self.logger.info(f"Interface successfully initialized and accessible at: http://{self._get_web_server_url()}")

    def _get_web_server_url(self):
        return f"{socket.gethostbyname(socket.gethostname())}:{self.server_port}"

    def run(self):
        # load routes
        load_routes()
        self.srv.serve_forever()

    def prepare_stop(self):
        self.srv.server_close()

    def stop(self):
        self.srv.shutdown()
