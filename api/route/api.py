"""
api.py
"""

from flask import Blueprint, jsonify, request, abort
from bson.objectid import ObjectId
from ..model.models import RequestExample, ErrorExample
from .user import api as user_api

api = Blueprint('api', __name__, url_prefix='/api')
api.register_blueprint(user_api)


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
