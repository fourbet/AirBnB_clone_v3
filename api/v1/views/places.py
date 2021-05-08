#!/usr/bin/python3
""" Cities """
from api.v1.views import app_views
import json
import models
from flask import jsonify, request
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """
        return (JSON)
        array of all Places objects of a City
    """
    objects_cities = models.storage.all(City)
    for k, v in objects_cities.items():
        if v.id == city_id:
            return jsonify([place.to_dict() for place in v.places])
    return jsonify(error='Not found'), 404


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
    object_cities = models.storage.all(City)
    for k, v in object_cities.items():
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
            atr = ['user_id', 'city_id', 'user_id', 'created_at', 'updated_at']
            for ke, val in content.items():
                if ke not in atr:
                    setattr(v, ke, val)
            # v.name = content['name']
            v.save()
            return jsonify(v.to_dict()), 200
    return jsonify(error='Not found'), 404


@app_views.route(
                '/places_search',
                methods=['POST'],
                strict_slashes=False)
def places_post():
    """
        retrieves all Place objects depending
        of the JSON in the body of the request
        The JSON can contain 3 optional keys:
            states: list of State ids
            cities: list of City ids
            amenities: list of Amenity ids
    """
    content = request.get_json()
    objects_places = models.storage.all(Place)
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if len(content) == 0 or all(value == 0 for value in content.values()):
        places = [place.to_dict() for k, place in objects_places.items()]
        return jsonify(places), 200

    # only states in JSON
    if 'states' in content and len(content['states']) > 0\
       and len(content) == 1:
        # states: [state_id, ....]
        places = []
        for state_id in content['states']:
            state = models.storage.get(State, state_id)
            cities = state.cities
            for city in cities:
                places += city.places
        return jsonify([place.to_dict() for place in places])

    # only cities
    if 'cities' in content and len(content['cities']) > 0\
       and len(content) == 1:
        places = []
        for city_id in content['cities']:
            city = models.storage.get(City, city_id)
            places += city.places
        return jsonify([place.to_dict() for place in places])

    # only amenities
    if 'amenities' in content and len(content['amenities']) > 0\
       and len(content) == 1:
        places = []
        for k, v in objects_places.items():
            count = 0
            for amenity in v.amenities:
                for amenity_id in content['amenities']:
                    if amenity.id == amenity_id:
                        count += 1
            if count == len(content['amenities']):
                places.append(v)
        return jsonify([place.to_dict() for place in places])

    # cities and states in JSON
    if 'cities' in content and 'states' in content and\
       len(content['states']) > 0 and len(content['cities']) > 0:
        places = []
        for state_id in content['states']:
            state = models.storage.get(State, state_id)
            cities = state.cities
            for city in cities:
                places += city.places
        for city_id in content['cities']:
            city = models.storage.get(City, city_id)
            not_in_place = 0
            for place in places:
                if place.city_id == city.id:
                    not_in_place = 1
            if not_in_place == 0:
                places += city.places
        # + amenities filter
        if 'amenities' in content:
            for place in places:
                count = 0
                for amenity in place.amenities:
                    for amenity_id in content['amenities']:
                        if amenity.id == amenity_id:
                            count += 1
                if count != len(content['amenities']):
                    places.remove(place)
        return jsonify([place.to_dict() for place in places])
