from distutils.version import LooseVersion

from flask import jsonify, render_template
from launcher.launcher_main import update_launcher

import launcher as launcher_module
from launcher import server_instance, VERSION, launcher_instance
from launcher.launcher_app import LauncherApp


@server_instance.route("/")
def home():
    return render_template('index.html',
                           launcher_version=VERSION)


@server_instance.route("/launcher")
def launcher():
    server_version = launcher_instance.get_launcher_server_version()
    if not server_version:
        server_version = "0"

    return render_template('launcher_card.html',
                           launcher_local_version=VERSION,
                           launcher_server_version=launcher_instance.get_launcher_server_version(),
                           is_up_to_date=LooseVersion(VERSION) >= LooseVersion(server_version))


@server_instance.route("/bot")
def bot():
    local_version = launcher_instance.get_bot_local_version()
    if not local_version:
        local_version = "0"

    server_version = launcher_instance.get_bot_server_version()
    if not server_version:
        server_version = "0"
    return render_template('bot_card.html',
                           bot_local_version=launcher_instance.get_bot_local_version(),
                           bot_server_version=launcher_instance.get_bot_server_version(),
                           bot_status=launcher_module.bot_instance,
                           is_up_to_date=LooseVersion(local_version) >= LooseVersion(server_version))


@server_instance.route("/news")
def news():
    return render_template('news_card.html')


@server_instance.route("/update")
def update():
    update_launcher(force=True)
    return jsonify('ok')


@server_instance.route("/install")
def install():
    LauncherApp.update_bot(launcher_module.bot_instance)
    return jsonify('ok')


@server_instance.route("/stop")
def stop():
    return jsonify()


@server_instance.route("/start")
def start():
    return jsonify()


@server_instance.route("/restart")
def restart():
    launcher_instance.restart_launcher()
    return jsonify('ok')
