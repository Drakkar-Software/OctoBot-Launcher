from flask import jsonify, render_template

from launcher import server_instance


@server_instance.route("/")
def home():
    return render_template('index.html')


@server_instance.route("/update")
def update():
    return jsonify()


@server_instance.route("/install")
def install():
    return jsonify()


@server_instance.route("/stop")
def stop():
    return jsonify()
