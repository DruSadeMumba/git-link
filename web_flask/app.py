#!/usr/bin/python3
""" Flask Application """
from flask import Flask
from flask_cors import CORS
from web_flask import app_views
from web_flask.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, threaded=True)
