#!/usr/bin/python3
"""Firebase user profile"""
from firebase_admin import db
from flask import redirect, url_for, render_template
from web_flask import app_views


@app_views.route("/profile/", strict_slashes=False)
@app_views.route("/profile/<uid>", strict_slashes=False)
def profile(uid=""):
    """Firebase profile page"""
    uid_ref = db.reference('users/' + uid)
    uid_data = uid_ref.get()
    if uid_data:
        return render_template('profile.html', uid=uid)
    elif uid == '':
        return redirect(url_for('app_views.login'))


@app_views.route("/back", strict_slashes=False)
def back():
    """Return to search"""
    return redirect(url_for('app_views.search'))


@app_views.route("/logout")
def logout():
    """Logout firebase user"""
    return redirect(url_for('app_views.search'))
