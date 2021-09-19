#!/usr/bin/python3
"""Amenities view - module"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route("/places", methods=["GET"],
                 strict_slashes=False)
def places_get():
    """Function that return a place dictionary object on JSON format"""
    palce_list = []
    places_dictionary = storage.all('Place').values()

    for obj in places_dictionary:
        amenitie = obj.to_dict()
        palce_list.append(amenitie)
    return jsonify(palce_list), 200


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_place_id(place_id):
    """Function that return a place object on JSON format"""
    places_data = storage.get("Place", place_id)

    if places_data:
        return jsonify(places_data.to_dict()), 200
    else:
        abort(404)


@app_views.route("/places/<string:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place_id(place_id):
    """Function that remove a amenitie object on JSON format"""
    places_data = storage.get("Place", place_id)

    if places_data is not None:
        storage.delete(places_data)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def places_create():
    """Function that creates and return a amenitie object on JSON format"""
    places_data = request.get_json()

    if not places_data:
        abort(400, {"Not a JSON"})
    if 'name' not in places_data:
        abort(400, {"Missing name"})

    new_place = Place(**places_data)
    storage.new(new_place)
    storage.save()
    places_dictionary = new_place.to_dict()

    return jsonify(places_dictionary), 201


@app_views.route("/places/<string:place_id>", methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id=None):
    """ Function that Update a state object and returns a JSON format"""
    place_obj = storage.get(Place, place_id)

    if place_obj is not None:
        place_data = request.get_json()
        if not place_data:
            return jsonify(error="Not a JSON"), 400
        for key, value in place_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(place_obj, key, value)
        place_obj.save()
        return jsonify(place_obj.to_dict())
    abort(404)
