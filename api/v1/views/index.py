#!/usr/bin/python3
""" Index """
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Return: status: OK
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def get_count():
    classes = {
        "amenity": Amenity,
        "city": City,
        "place": Place,
        "review": Review,
        "state": State,
        "user": User,
    }
    obj_count = {}

    for key, value in classes.items():
        obj_count[key] = storage.count(value)
    return jsonify(obj_count)
