#!/usr/bin/python3
"""Amenities view - module"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def amenities_get():
    """Function that return a amenity dictionary object on JSON format"""
    ameniti_list = []
    amenities_dictionary = storage.all('Amenity').values()

    for obj in amenities_dictionary:
        amenitie = obj.to_dict()
        ameniti_list.append(amenitie)
    return jsonify(ameniti_list), 200


@app_views.route("/amenities/<string:amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """Function that return a amenity object on JSON format"""
    amenities_data = storage.get("Amenity", amenity_id)

    if amenities_data:
        return jsonify(amenities_data.to_dict()), 200
    else:
        abort(404)


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_id(amenity_id):
    """Function that remove a amenitie object on JSON format"""
    amenities_data = storage.get("Amenity", amenity_id)

    if amenities_data is not None:
        storage.delete(amenities_data)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def amenities_create():
    """Function that creates and return a amenitie object on JSON format"""
    amenities_data = request.get_json()

    if not amenities_data:
        abort(400, {"Not a JSON"})
    if 'name' not in amenities_data:
        abort(400, {"Missing name"})

    new_amenity = Amenity(**amenities_data)
    storage.new(new_amenity)
    storage.save()
    amenities_dictionary = new_amenity.to_dict()

    return jsonify(amenities_dictionary), 201


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """Function that updates a Amenties dictionary and retireve
    in Json Format"""
    amenities_data = request.get_json()
    amenity = storage.get("Amenity", amenity_id)

    if not amenity:
        abort(404)
    if not amenities_data:
        abort(400, {"Not a JSON"})

    if 'name' in amenities_data:
        for key, value in amenities_data.items():
            if key not in ['id', 'amenity_id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()

    update_dictionary = amenity.to_dict()
    return jsonify(update_dictionary), 200
