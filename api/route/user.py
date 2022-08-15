from flask import Blueprint, jsonify, request, abort
from bson import ObjectId
from ..model.models import *

api = Blueprint('user', __name__, url_prefix='/user')


@api.route('/', methods=['GET'])
def getUsers():
    users = UserExample.objects
    return jsonify(users)


@api.route('/<userID>', methods=['GET'])
def getUserInfo(userID):
    """Get detailed info for a specific user
    ---
    parameters:
        - name: id
          in: query
          type: string
          required: true
    """

    try:
        user = UserExample.objects(_id=ObjectId(userID)).first()
        if not user:
            abort(400)

        user_events = ErrorExample.objects(user=ObjectId(userID))
        return jsonify({'user': user, 'events': user_events})
    except Exception as e:
        print(e)
        abort(400)
