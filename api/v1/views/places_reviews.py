#!/usr/bin/python3
"""Reviews view  - module"""

from models import storage
from models.review import Review
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, request, abort

from models.user import User


@app_views.route("/reviews", methods=["GET"])
def reviews_get():
    """Function that return  the list of all Review objects of a Place
    JSON format"""
    reviews_list = []
    review_dictionary = storage.all(Review).values()

    for obj in review_dictionary:
        review = obj.to_dict()
        reviews_list.append(review)

    return jsonify(reviews_list), 200


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_reviews_by_places(place_id):
    """Function that return a review object"""
    review_list = []

    if not storage.get(Place, place_id):
        abort(404)

    for review in storage.all(Review).values():
        if review.to_dict()["place_id"] == place_id:
            review_list.append(review.to_dict())

    return jsonify(review_list), 200


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review_id(review_id):
    """Returns a Review object based on: review_id"""
    review_data = storage.get(Review, review_id)

    if review_data:
        return jsonify(review_data.to_dict()), 200
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review_id(review_id):
    """Function that remove a Review object"""
    review_data = storage.get(Review, review_id)

    if review_data:
        storage.delete(review_data)
        storage.save()

        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Function that create a review object and returns a JSON format"""
    review_data = request.get_json()

    if not storage.get(Place, place_id):
        abort(404)
    if not review_data:
        return jsonify(error="Not a JSON"), 400
    if 'user_id' not in review_data:
        return jsonify(error="Missing user_id"), 400
    if not storage.get(User, review_data["user_id"]):
        abort(404)
    if 'text' not in review_data:
        return jsonify(error="Missing text"), 400

    review_data["place_id"] = place_id
    new_rev = Review(**review_data)
    storage.new(new_rev)
    storage.save()

    return jsonify(new_rev.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_reviews(review_id):
    """Function that Review a place object and returns a JSON format"""
    review_dictionary = request.get_json()
    review_data = storage.get(Review, review_id)

    if not review_data:
        abort(404)
    if not review_dictionary:
        return jsonify(error="Not a JSON"), 400

    for key, value in review_dictionary.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review_data, key, value)
            storage.save()

    dictionary_update = review_data.to_dict()
    return jsonify(dictionary_update), 200
