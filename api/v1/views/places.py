#!/usr/bin/python3
""" Cities """
from api.v1.views import app_views
import json
import models
from flask import jsonify, request
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """
        return (JSON)
        array of all Places objects of a City
    """
    arr = []
    objects_places = models.storage.all(Place)
    for k, v in objects_places.items():
        if v.city_id == city_id:
            arr.append(v.to_dict())
    if arr == []:
        return jsonify(error='Not found'), 404
    return jsonify(arr)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place(place_id):
    """
        return (JSON)
        dict of the object from the place_id
    """
    objects_places = models.storage.all(Place)
    for k, v in objects_places.items():
        if v.id == place_id:
            return jsonify(v.to_dict())
    return jsonify(error='Not found'), 404


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """
        return (JSON)
        dict of the object from the place_id
    """
    objects_places = models.storage.all(Place)
    for k, v in objects_places.items():
        if v.id == place_id:
            models.storage.delete(v)
            models.storage.save()
            return jsonify({}), 200
    return jsonify(error='Not found'), 404


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """
        create a new place
        header value: {name = value}
        return (JSON)
    """
    content = request.get_json()
    city_not_present = 1
    object_places = models.storage.all(Place)
    for k, v in object_places.items():
        if v.id == city_id:
            city_not_present = 0
    if city_not_present:
        return jsonify(error="Not found"), 404
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'name' not in content:
        return jsonify(error='Missing name'), 400
    if 'user_id' not in content:
        return jsonify(error='Missing user_id'), 400
    user_not_present = 1
    object_users = models.storage.all(User)
    for k, v in object_users.items():
        if v.id == content['user_id']:
            user_not_present = 0
    if user_not_present:
        return jsonify(error="Not found"), 404
    place = Place(name=content['name'], user_id=content['user_id'],
                  city_id=city_id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def place_put(place_id):
    """
        update a place
        header value: {name = value}
        return (JSON)
    """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    objects_places = models.storage.all(Place)
    for k, v in objects_places.items():
        if v.id == place_id:
            v.name = content['name']
            v.save()
            return jsonify(v.to_dict()), 200
    return jsonify(error='Not found'), 404
