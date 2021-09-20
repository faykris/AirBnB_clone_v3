#!/usr/bin/python3
"""Places - view module"""

from models import storage
from models.place import Place
from models.state import City
from api.v1.views import app_views
from flask import jsonify, request, abort

from models.user import User


@app_views.route("/cities/<string:city_id>/places", methods=["GET"])
def places_by_cities_get(city_id):
    """Function that return Place related to teh cities
    object on JSON format"""
    places_list = []

    if not storage.get(City, city_id):
        abort(404)

    for place in storage.all(Place).values():
        if place.to_dict()["city_id"] == city_id:
            places_list.append(place.to_dict())

    return jsonify(places_list), 200


@app_views.route("/places/<string:place_id>", methods=["GET"])
def get_place_id(place_id):
    """Function that return a Place object id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.route("/places/<string:place_id>", methods=["DELETE"])
def delete_place_id(place_id):
    """Function that remove a Place object"""
    place_delete = storage.get(Place, place_id)

    if place_delete:
        storage.delete(place_delete)
        storage.save()
        return jsonify({}), 200

    else:
        abort(404)


@app_views.route("/cities/<string:city_id>/places", methods=["POST"])
def create_place(city_id):
    """Function that create a place object and returns a JSON format"""
    place_data = request.get_json()
    if not storage.get(City, city_id):
        abort(404)
    if not place_data:
        return jsonify(error="Not a JSON"), 400
    if 'user_id' not in place_data:
        return jsonify(error="Missing user_id"), 400
    if not storage.get(User, place_data["user_id"]):
        abort(404)
    if 'name' not in place_data:
        return jsonify(error="Missing name"), 400

    place_data["city_id"] = city_id
    new_place = Place(**place_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<string:place_id>", methods=["PUT"])
def update_places(place_id):
    """Function that Update a place object and returns a JSON format"""
    place_dictionary = request.get_json()
    place_update = storage.get(Place, place_id)

    if not place_update:
        abort(404)
    if not place_dictionary:
        return jsonify(error="Not a JSON"), 400

    for key, value in place_dictionary.items():
        if key not in ['id', 'user_id', 'city_id',
                       'created_at', 'updated_at']:
            setattr(place_update, key, value)
            storage.save()

    update_dictionary = place_update.to_dict()

    return jsonify(update_dictionary), 200
