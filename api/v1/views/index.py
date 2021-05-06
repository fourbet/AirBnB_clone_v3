#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
import json
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """ return a JSON """
    return jsonify(status="OK")
