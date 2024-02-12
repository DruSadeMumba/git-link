#!/usr/bin/env python3
"""Firebase user signup"""

from flask import render_template, jsonify
from web_flask import app_views
from web_flask.config import Config


@app_views.route("/signup", strict_slashes=False)
def signup():
    return render_template("sign-up.html")


@app_views.route('/firebase-config')
def get_firebase_config():
    return jsonify(Config.FIREBASE_CONFIG)
