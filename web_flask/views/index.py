#!/usr/bin/python3
"""App slash screen"""
from flask import render_template
from web_flask import app_views


@app_views.route("/")
def splash():
    return render_template("index.html")
