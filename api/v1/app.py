#!/usr/bin/python3
""" Create app, blueprint and run app"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app)


cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(e):
    """ return 404 status code error if page not found """
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def teardown(exception):
    """ remove the current SQLAlchemy Session"""
    storage.close()

if __name__ == '__main__':
    if os.getenv('HBNB_API_HOST') is not None:
        h = os.getenv('HBNB_API_HOST')
    else:
        h = '0.0.0.0'
    if os.getenv('HBNB_API_PORT') is not None:
        p = os.getenv('HBNB_API_PORT')
    else:
        p = '5000'
    app.run(host=h, port=p, threaded=True)
