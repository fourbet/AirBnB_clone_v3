#!/usr/bin/python3
""" States """
from api.v1.views import app_views
import json
import models
from flask import jsonify, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """
        return (JSON)
        array of all dict of all objects
    """
    arr = []
    objects_states = models.storage.all(State)
    for k, v in objects_states.items():
        arr.append(v.to_dict())
    return jsonify(arr)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """
        return (JSON)
        dict of the object from the state_id
    """
    objects_states = models.storage.all(State)
    for k, v in objects_states.items():
        if v.id == state_id:
            return jsonify(v.to_dict())
    return jsonify(error='Not found'), 404


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False)
def state_delete(state_id):
    """
        return (JSON)
        dict of the object from the state_id
    """
    objects_states = models.storage.all(State)
    for k, v in objects_states.items():
        if v.id == state_id:
            models.storage.delete(v)
            models.storage.save()
            return jsonify({}), 200
    return jsonify(error='Not found'), 404


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """
        create a new state
        header value: {name = value}
        return (JSON)
    """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'name' in content:
        state = State(name=content['name'])
        state.save()
        return jsonify(state.to_dict()), 201
    return jsonify(error='Missing name'), 400


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """
        update a state
        header value: {name = value}
        return (JSON)
    """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    objects_states = models.storage.all(State)
    for k, v in objects_states.items():
        if v.id == state_id:
            v.name = update(content)
            v.save()
            return jsonify(v.to_dict()), 200
    return jsonify(error='Not Found'), 404
