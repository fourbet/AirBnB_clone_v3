#!/usr/bin/python3
""" Place Amenities """
from api.v1.views import app_views
import json
import models
from flask import jsonify, request
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity
import os


@app_views.route(
    '/places/<place_id>/amenities',
    methods=['GET'],
    strict_slashes=False)
def place_amenities(place_id):
    """
        return (JSON)
        array of all amenities to a place
    """
    object_places = models.storage.all(Place)
    for k, v in object_places.items():
        if v.id == place_id:
            if os.getenv('HBNB_TYPE_STORAGE') == "db":
                all_amenities = [x.to_dict() for x in v.amenities]
            else:
                all_amenities = v.amenity_ids
            return jsonify(all_amenities)
    return jsonify(error='Not found'), 404


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False)
def place_amenity(place_id, amenity_id):
    """
        return (JSON)
        delete amenity from a place
    """
    objects_places = models.storage.all(Place)
    for k, v in objects_places.items():
        if v.id == place_id:
            all_amenities = models.storage.all(Amenity)
            tmp = 'Amenity.' + amenity_id
            if tmp not in all_amenities:
                return jsonify(error='Not found'), 404
            if os.getenv('HBNB_TYPE_STORAGE') == "db":
                all_amenities = v.amenities
            else:
                all_amenities = v.amenity_ids
            for each in all_amenities:
                if each.id == amenity_id:
                    models.storage.delete(each)
                    models.storage.save()
                    return jsonify({}), 200
            return jsonify(error='Not found'), 404
    return jsonify(error='Not found'), 404


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['POST'],
    strict_slashes=False)
def place_amenity_post(place_id, amenity_id):
    """
        link an amenity to a place
        return (JSON)
    """
    objects_places = models.storage.all(Place)
    for k, v in objects_places.items():
        if v.id == place_id:
            all_amenities = models.storage.all(Amenity)
            tmp = 'Amenity.' + amenity_id
            if tmp not in all_amenities:
                return jsonify(error='Not found'), 404
            if os.getenv('HBNB_TYPE_STORAGE') == "db":
                all_amenities = v.amenities
            else:
                all_amenities = v.amenity_ids
            for each in all_amenities:
                if each.id == amenity_id:
                    return jsonify(each.to_dict), 200
            if os.getenv('HBNB_TYPE_STORAGE') == "db":
                v.amenities.append(all_amenities[tmp])
                v.save()
                return jsonify(all_amenities[tmp].to_dict()), 201
            else:
                v.amenity_ids.append(all_amenities[tmp])
                v.save()
                return jsonify(all_amenities[tmp].to_dict()), 201
            return jsonify(error='Not found'), 404
    return jsonify(error='Not found'), 404
