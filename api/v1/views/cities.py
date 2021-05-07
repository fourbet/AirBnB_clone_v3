#!/usr/bin/python3
""" Cities """
from api.v1.views import app_views
import json
import models
from flask import jsonify, request
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def states_city(state_id):
    """
        return (JSON)
        array of all City objects of a State
    """
    arr = []
    objects_cities = models.storage.all(City)
    for k, v in objects_cities.items():
        if v.state_id == state_id:
            arr.append(v.to_dict())
    if arr == []:
        return jsonify(error='Not found'), 404
    return jsonify(arr)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city(city_id):
    """
        return (JSON)
        dict of the object from the city_id
    """
    objects_cities = models.storage.all(City)
    for k, v in objects_cities.items():
        if v.id == city_id:
            return jsonify(v.to_dict())
    return jsonify(error='Not found'), 404


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id):
    """
        return (JSON)
        dict of the object from the city_id
    """
    objects_cities = models.storage.all(City)
    for k, v in objects_cities.items():
        if v.id == city_id:
            models.storage.delete(v)
            models.storage.save()
            return jsonify({}), 200
    return jsonify(error='Not found'), 404


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    """
        create a new city
        header value: {name = value}
        return (JSON)
    """
    content = request.json
    state_not_present = 1
    object_states = models.storage.all(State)
    for k, v in object_states.items():
        if v.id == state_id:
            state_not_present = 0
    if state_not_present:
        return jsonify(error="Not found"), 404
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'name' in content:
        city = City(name=content['name'], state_id=state_id)
        city.save()
        return jsonify(city.to_dict()), 201
    return jsonify(error='Missing name'), 400


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def city_put(city_id):
    """
        update a city
        header value: {name = value}
        return (JSON)
    """
    content = request.json
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'name' in content:
        objects_cities = models.storage.all(City)
        for k, v in objects_cities.items():
            if v.id == city_id:
                v.name = content['name']
                v.save()
                return jsonify(v.to_dict()), 200
    return jsonify(error='Missing name'), 400
