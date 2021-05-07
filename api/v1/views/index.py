#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
import json
import models
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """
        return (JSON)
        a dict with status and ok
    """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'])
def stats():
    """
        return (JSON)
        a dict of all classes and the number of objects for each classes
    """
    dict_classes = {
            City: 'cities',
            Amenity: 'amenities',
            Place: 'places',
            Review: 'reviews',
            State: 'states',
            User: 'users'
    }
    dict_count = {}
    for key, value in dict_classes.items():
        number_objects = models.storage.count(key)
        dict_count[value] = number_objects
    return jsonify(dict_count)
