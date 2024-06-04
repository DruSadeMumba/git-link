#!/usr/bin/python3
"""Api blueprint"""
from flask import Blueprint, Flask

app_views = Blueprint('app_views', __name__, url_prefix='/')
app = Flask(__name__)

from web_flask.views.index import *
from web_flask.views.signup import *
from web_flask.views.login import *
from web_flask.views.profile import *
from web_flask.views.gituser import *
from web_flask.views.gitrepo import *
