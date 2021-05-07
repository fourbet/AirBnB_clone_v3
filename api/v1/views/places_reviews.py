#!/usr/bin/python3
""" Reviews """
from api.v1.views import app_views
import json
import models
from flask import jsonify, request
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False)
def reviews(place_id):
    """
        return (JSON)
        array of all reviews
    """
    arr = []
    object_places = models.storage.all(Place)
    for k, v in object_places.items():
        if v.id == place_id:
            all_reviews = [x.to_dict() for x in v.reviews]
            return jsonify(all_reviews)
    return jsonify(error='Not found'), 404


@app_views.route(
    '/reviews/<review_id>',
    methods=['GET'],
    strict_slashes=False)
def review(review_id):
    """
        return (JSON)
        dict of the object from the review_id
    """
    objects_reviews = models.storage.all(Review)
    for k, v in objects_reviews.items():
        if v.id == review_id:
            return jsonify(v.to_dict())
    return jsonify(error='Not found'), 404


@app_views.route(
    '/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False)
def reviews_delete(review_id):
    """
        return (JSON)
        dict of the object from the review_id
    """
    objects_review = models.storage.all(Review)
    for k, v in objects_review.items():
        if v.id == review_id:
            models.storage.delete(v)
            models.storage.save()
            return jsonify({}), 200
    return jsonify(error='Not found'), 404


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False)
def reviews_post(place_id):
    """
        create a new review
        header value: {text = value, place_id = value, user_id=value}
        return (JSON)
    """
    content = request.get_json()
    objects_places = models.storage.all(Place)
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    for k, v in objects_places.items():
        if v.id == place_id:
            if 'user_id' not in content:
                return jsonify(error='Missing user_id'), 400
            objects_users = models.storage.all(User)
            tmp = 'User.' + content['user_id']
            if tmp not in objects_users:
                return jsonify(error='Not found'), 404
            if 'text' not in content:
                return jsonify(error='Missing text'), 400
            review = Review(
                     user_id=content['user_id'],
                     place_id=place_id,
                     text=content['text'])
            review.save()
            return jsonify(review.to_dict()), 201
    return jsonify(error='Not found'), 404


@app_views.route(
    '/reviews/<review_id>',
    methods=['PUT'],
    strict_slashes=False)
def reviews_put(review_id):
    """
        update a review
        header value: {text=value}
        return (JSON)
    """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    objects_reviews = models.storage.all(Review)
    for k, v in objects_reviews.items():
        if v.id == review_id:
            v.text = content['text']
            v.save()
            return jsonify(v.to_dict()), 200
    return jsonify(error='Not Found'), 404
