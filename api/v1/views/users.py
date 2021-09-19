#!/usr/bin/python3
"""Amenities view - module"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def users_get():
    """Function that return a user dictionary object on JSON format"""
    user_list = []
    users_dictionary = storage.all('User').values()

    for obj in users_dictionary:
        user = obj.to_dict()
        user_list.append(user)
    return jsonify(user_list), 200


@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user_id(user_id):
    """Function that return a user object on JSON format"""
    users_data = storage.get("User", user_id)

    if users_data:
        return jsonify(users_data.to_dict()), 200
    else:
        abort(404)


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user_id(user_id):
    """Function that remove a amenitie object on JSON format"""
    users_data = storage.get("User", user_id)

    if users_data is not None:
        storage.delete(users_data)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def users_create():
    """Function that creates and return a amenitie object on JSON format"""
    users_data = request.get_json()

    if not users_data:
        abort(400, {"Not a JSON"})
    if 'name' not in users_data:
        abort(400, {"Missing name"})

    new_user = User(**users_data)
    storage.new(new_user)
    storage.save()
    users_dictionary = new_user.to_dict()

    return jsonify(users_dictionary), 201


@app_views.route("/users/<string:user_id>", methods=["PUT"],
                 strict_slashes=False)
def user_put(user_id=None):
    """ Function that Update a state object and returns a JSON format"""
    user_obj = storage.get(User, user_id)

    if user_obj is not None:
        user_data = request.get_json()
        if not user_data:
            return jsonify(error="Not a JSON"), 400
        for key, value in user_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user_obj, key, value)
        user_obj.save()
        return jsonify(user_obj.to_dict())
    abort(404)
