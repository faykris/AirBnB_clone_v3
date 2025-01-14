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
    amenities_list = []
    amenities_dictionary = storage.all(Amenity).values()

    for obj in amenities_dictionary:
        amenity = obj.to_dict()
        amenities_list.append(amenity)
    return jsonify(amenities_list), 200


@app_views.route("/amenities/<string:amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """Function that return a amenity object on JSON format"""
    amenities_data = storage.get(Amenity, amenity_id)

    if amenities_data:
        return jsonify(amenities_data.to_dict()), 200
    else:
        abort(404)


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_id(amenity_id):
    """Function that remove a amenity object on JSON format"""
    amenities_data = storage.get(Amenity, amenity_id)

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
def amenity_put(amenity_id=None):
    """ Function that Update a state object and returns a JSON format"""
    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is not None:
        amenity_data = request.get_json()
        if not amenity_data:
            return jsonify(error="Not a JSON"), 400
        for key, value in amenity_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity_obj, key, value)
        amenity_obj.save()
        return jsonify(amenity_obj.to_dict())
    abort(404)
