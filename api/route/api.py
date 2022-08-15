"""
api.py
"""

from flask import Blueprint, jsonify, request, abort
from bson.objectid import ObjectId
from bson.errors import BSONError
from ..model.models import UserExample, RequestExample, ErrorExample

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def getUsers():
    users = UserExample.objects
    return jsonify(users)


@api.route('/user', methods=['GET'])
def getUserInfo():
    userID = request.args.get('id')

    if not userID:
        abort(404)

    try:
        user = UserExample.objects(_id=ObjectId(userID)).first()
        if not user:
            abort(404)

        user_events = ErrorExample.objects(user=ObjectId(userID))
        return jsonify({'user': user, 'events': user_events})
    except Exception as e:
        print(e)
        abort(404)


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
