"""
api.py
"""

from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from ..model.models import UserExample, RequestExample, ErrorExample

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def getUsers():
    users = UserExample.objects
    return jsonify(users)


@api.route('/request', methods=['GET'])
def getRequest():
    reqs = RequestExample.objects
    return jsonify(reqs)


@api.route('/errors', methods=['GET'])
def getErrors():
    category = request.args.get('category')
    userID = request.args.get('userid')

    if category:
        errors = ErrorExample.objects(category=category)
    elif userID:
        errors = ErrorExample.objects(user=ObjectId(userID))
    else:
        errors = ErrorExample.objects

    return jsonify(errors)
