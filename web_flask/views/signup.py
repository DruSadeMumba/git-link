#!/usr/bin/env python3
"""Firebase user signup"""
from flask import render_template
from web_flask import app_views


@app_views.route("/signup", strict_slashes=False)
def signup():
    return render_template("sign-up.html")
