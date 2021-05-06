#!/usr/bin/python3
""" Create app, blueprint and run app"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.register_blueprint(app_views)


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
