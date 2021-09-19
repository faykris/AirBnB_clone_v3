#!/usr/bin/python3
"""Amenities view - module"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'],
                 strict_slashes=False)
def amenities_by_state(state_id=None):
    """Function that return a amenity object on JSON format"""
    if state_id is not None:
        state_obj = storage.get(State, state_id)
        if state_obj is not None:
            amenities_list = []
            for key, value in storage.all(Amenity).items():
                if state_obj.id == value.state_id:
                    amenities_list.append(value.to_dict())
            return jsonify(amenities_list)
    abort(404)


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenity_get(amenity_id=None):
    """Function that return a amenity object on JSON format"""
    if amenity_id is not None:
        amenity_obj = storage.get(Amenity, amenity_id)
        if amenity_obj is not None:
            return jsonify(amenity_obj.to_dict())
    abort(404)


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id=None):
    """Function that remove a amenity object on JSON format"""
    if amenity_id is not None:
        amenity_obj = storage.get(Amenity, amenity_id)
        if amenity_obj is not None:
            storage.delete(amenity_obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def amenity_post(state_id):
    """Function that creates and return a amenity object on JSON format"""
    if state_id is not None and storage.get(State, state_id) is not None:
        amenity_data = request.get_json()
        if not amenity_data:
            return jsonify(error="Not a JSON"), 400
        amenity_name = amenity_data.get("name")
        if amenity_name is None:
            return jsonify(error="Missing name"), 400
        amenity_data["state_id"] = state_id
        amenity_new = Amenity(**amenity_data)
        if amenity_new.state_id == state_id:
            amenity_new.save()
            return jsonify(amenity_new.to_dict()), 201
    abort(404)


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
