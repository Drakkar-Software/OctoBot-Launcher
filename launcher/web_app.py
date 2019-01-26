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

from launcher import DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT, load_routes, server_instance


class WebApp(threading.Thread):
    def __init__(self, web_ip=DEFAULT_SERVER_IP, web_port=DEFAULT_SERVER_PORT):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app = None

        self.server_ip = web_ip
        self.server_port = web_port

    def run(self):
        # Define the WSGI application object
        self.app = server_instance

        # load routes
        load_routes()

        self.app.run(host=self.server_ip,
                     port=self.server_port,
                     debug=False,
                     threaded=True,
                     use_reloader=False)

    def stop(self):
        # func = request.environ.get('werkzeug.server.shutdown')
        # if func is None:
        #     raise RuntimeError('Not running with the Werkzeug Server')
        # func()
        pass
