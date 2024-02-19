#!/usr/bin/python3
"""Firebase login"""
from flask import render_template
from web_flask import app_views


@app_views.route("/login", strict_slashes=False)
def login():
    """Firebase login"""
    return render_template("login.html")
