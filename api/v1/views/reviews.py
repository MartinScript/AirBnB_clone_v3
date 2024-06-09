#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review


@app_views.route("/reviews", methods=["GET"], strict_slashes=False)
def get_review():
    """Retrieves the list of all Review objects"""
    all_reviews = storage.all(Review).values()
    list_review = []
    for review in all_reviews:
        list_review.append(review.to_dict())
    return jsonify(list_review)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review_id(review_id):
    """Retrieves a Review by id"""
    review = storage.get(review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review_id(review_id):
    """Deletes a Review object by id"""
    review = storage.get(review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/reviews", methods=["POST"], strict_slashes=False)
def create_review():
    """Creates a Review"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not "name" in request.json():
        abort(400, "Missing name")

    review = request.json()
    instance = Review(**review)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(review), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by id"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not storage.get(review, review_id):
        abort(404)

    review = storage.get(review, review_id)
    review_data = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in review_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()

    return make_response(jsonify(review), 200)