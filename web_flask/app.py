#!/usr/bin/python3
""" Flask Application """
import firebase_admin
from firebase_admin import credentials
from flask import Flask
from flask_cors import CORS
from web_flask.config import Config
from web_flask import app_views

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
app.register_blueprint(app_views)
cred = credentials.Certificate("web_flask/views/git-link-d9cc9-firebase-adminsdk-o2gwi-821d140e51.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://git-link-d9cc9-default-rtdb.firebaseio.com/'})
cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, threaded=True)
