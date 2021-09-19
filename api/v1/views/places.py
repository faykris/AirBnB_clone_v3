#!/usr/bin/python3
"""Places - view module"""

from models import storage
from models.place import Place
from models.state import City
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/places", methods=["GET"])
def places_get():
    """Function that return  the list of all Place objects of a City
    JSON format"""
    places_list = []
    places_dict = storage.all(Place).values()

    for obj in places_dict:
        place = obj.to_dict()
        places_list.append(place)

    return jsonify(places_list), 200


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def places_by_cities_get(city_id):
    """Function that return Place releated to teh cities
    object on JSON format"""
    palces_list = []

    if not storage.get(City, city_id):
        abort(404)

    for place in storage.all(Place).values():
        if place.to_dict()["city_id"] == city_id:
            palces_list.append(place.to_dict())

    return jsonify(palces_list), 200


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place_id(place_id):
    """Function that remove a Place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place_id(place_id):
    """Function that remove a Place object"""
    place_delete = storage.get(Place, place_id)

    if place_delete:
        storage.delete(place_delete)
        storage.save()
        return jsonify({}), 200

    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """ Function that create a place object and returns a JSON format"""
    place_data = request.get_json()

    if not storage.get(City, city_id):
        abort(404)
    if not place_data:
        abort(400, {"Not a JSON"})
    if 'user_id' not in place_data:
        abort(400, {"Missing user_id"})
    if not storage.get("User", place_data["user_id"]):
        abort(404)
    if 'name' not in place_data:
        abort(400, {"Missing name"})

    place_data["city_id"] = city_id
    new_place = Place(**place_data)
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_places(place_id):
    """Function that Update a place object and returns a JSON format"""
    place_dictionary = request.get_json()
    place_update = storage.get(Place, place_id)

    if not place_update:
        abort(404)
    if not place_dictionary:
        abort(400, {"Not a JSON"})

    for key, value in place_dictionary.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(place_update, key, value)
            storage.save()

    update_idctionary = place_update.to_dict()

    return jsonify(update_idctionary), 200
