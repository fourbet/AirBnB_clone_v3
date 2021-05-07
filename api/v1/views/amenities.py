#!/usr/bin/python3
""" Amenities """
from api.v1.views import app_views
import json
import models
from flask import jsonify, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """
        return (JSON)
        array of all dict of all objects
    """
    arr = []
    objects_amenities = models.storage.all(Amenity)
    for k, v in objects_amenities.items():
        arr.append(v.to_dict())
    return jsonify(arr)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False)
def amenity(amenity_id):
    """
        return (JSON)
        dict of the object from the amenity_id
    """
    objects_amenities = models.storage.all(Amenity)
    for k, v in objects_amenities.items():
        if v.id == amenity_id:
            return jsonify(v.to_dict())
    return jsonify(error='Not found'), 404


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False)
def amenity_delete(amenity_id):
    """
        return (JSON)
        dict of the object from the amenity_id
    """
    objects_amenities = models.storage.all(Amenity)
    for k, v in objects_amenities.items():
        if v.id == amenity_id:
            models.storage.delete(v)
            models.storage.save()
            return jsonify({}), 200
    return jsonify(error='Not found'), 404


@app_views.route(
    '/amenities',
    methods=['POST'],
    strict_slashes=False)
def amenity_post():
    """
        create a new amenity
        header value: {name = value}
        return (JSON)
    """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'name' in content:
        amenity = Amenity(name=content['name'])
        amenity.save()
        return jsonify(amenity.to_dict()), 201
    return jsonify(error='Missing name'), 400


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False)
def amenity_put(amenity_id):
    """
        update a state
        header value: {name = value}
        return (JSON)
    """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'name' in content:
        objects_amenities = models.storage.all(Amenity)
        for k, v in objects_amenities.items():
            if v.id == state_id:
                v.name = content['name']
                v.save()
                return jsonify(v.to_dict()), 200
        return jsonify(error='Not Found'), 404
