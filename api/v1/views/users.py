#!/usr/bin/python3
""" Users """
from api.v1.views import app_views
import json
import models
from flask import jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """
        return (JSON)
        array of all dict of all objects
    """
    arr = []
    objects_amenities = models.storage.all(User)
    for k, v in objects_amenities.items():
        arr.append(v.to_dict())
    return jsonify(arr)


@app_views.route(
    '/users/<user_id>',
    methods=['GET'],
    strict_slashes=False)
def user(user_id):
    """
        return (JSON)
        dict of the object from the user_id
    """
    objects_users = models.storage.all(User)
    for k, v in objects_users.items():
        if v.id == user_id:
            return jsonify(v.to_dict())
    return jsonify(error='Not found'), 404


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False)
def users_delete(user_id):
    """
        return (JSON)
        dict of the object from the user_id
    """
    objects_users = models.storage.all(User)
    for k, v in objects_users.items():
        if v.id == user_id:
            models.storage.delete(v)
            models.storage.save()
            return jsonify({}), 200
    return jsonify(error='Not found'), 404


@app_views.route(
    '/users',
    methods=['POST'],
    strict_slashes=False)
def users_post():
    """
        create a new user
        header value: {email = value, password = value}
        return (JSON)
    """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'email' in content:
        email = content['email']
    else:
        return jsonify(error='Missing email'), 400
    if 'password' in content:
        password = content['password']
    else:
        return jsonify(error='Missing password'), 400
    user = User(email=email, password=password)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False)
def users_put(user_id):
    """
        update an user
        header value: {password=password}
        return (JSON)
    """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    objects_users = models.storage.all(User)
    for k, v in objects_users.items():
        if v.id == user_id:
            atr = ['user_id', 'id', 'city_id', 'created_at', 'updated_at']
            for ke, val in content.items():
                if ke not in atr:
                    setattr(v, ke, val)
            v.save()
            return jsonify(v.to_dict()), 200
    return jsonify(error='Not Found'), 404
