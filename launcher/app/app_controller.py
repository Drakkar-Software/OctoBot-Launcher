from flask import jsonify, render_template

import launcher as launcher_module
from entrypoint import update_launcher
from launcher import server_instance, VERSION, launcher_instance, REDUCE_GITHUB_REQUESTS
from launcher.tools.environment import update_tentacles
from launcher.tools.github import GithubOctoBot, GithubLauncher
from launcher.tools.version import OctoBotVersion
from launcher.app.app_model import is_up_to_date
from launcher.tools.octobot_connector import OctoBotConnector


@server_instance.route("/")
def home():
    return render_template('index.html',
                           launcher_version=VERSION)


@server_instance.route("/launcher")
def launcher():
    server_version = None if REDUCE_GITHUB_REQUESTS else GithubLauncher().get_current_server_version()
    if not server_version:
        server_version = "0"

    return render_template('launcher_card.html',
                           launcher_local_version=VERSION,
                           launcher_server_version=server_version,
                           is_up_to_date=is_up_to_date(VERSION, server_version))


@server_instance.route("/bot")
def bot():
    bot_connector = OctoBotConnector()
    is_bot_alive = launcher_instance.is_bot_alive() or bot_connector.is_alive()
    if is_bot_alive:
        local_version = bot_connector.get_current_version(allow_retry=True)
        bot_url = bot_connector.get_web_interface_url()
    else:
        local_version = OctoBotVersion().get_current_version()
        bot_url = None
    if not local_version:
        local_version = "0"

    server_version = None if REDUCE_GITHUB_REQUESTS else GithubOctoBot().get_current_server_version()
    if not server_version:
        server_version = "0"
    return render_template('bot_card.html',
                           bot_local_version=local_version,
                           bot_server_version=server_version,
                           bot_status=is_bot_alive,
                           bot_url=bot_url,
                           is_up_to_date=is_up_to_date(local_version, server_version))


@server_instance.route("/news")
def news():
    return render_template('news_card.html')


@server_instance.route("/update")
def update():
    update_launcher()
    return jsonify('ok')


@server_instance.route("/install")
def install():
    launcher_instance.update_bot(launcher_module.bot_instance)
    return jsonify('ok')


@server_instance.route("/tentacles")
def tentacles():
    update_tentacles(OctoBotVersion().get_local_binary())
    return jsonify('ok')


@server_instance.route("/stop")
def stop():
    launcher_instance.stop_bot()
    return jsonify('ok')


@server_instance.route("/start")
def start():
    launcher_instance.start_bot_handler()
    return jsonify('ok')


@server_instance.route("/restart")
def restart():
    launcher_instance.restart_launcher()
    return jsonify('ok')


@server_instance.route("/stop_launcher")
def stop_launcher():
    launcher_instance.stop_launcher()
    return jsonify('ok')


@server_instance.route("/progress")
def progess():
    return jsonify(launcher_module.processing)
