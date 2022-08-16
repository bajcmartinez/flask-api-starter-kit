from flask import Blueprint, jsonify, request, abort
from bson import ObjectId
from bson import errors as bsonError
from ..model.models import *

api = Blueprint('user', __name__, url_prefix='/user')


@api.route('/', methods=['GET'])
def get_users():
    users = User.objects
    return jsonify({'data': [user.to_dict() for user in users], 'status': True, 'code': 200})


@api.route('/<userID>', methods=['GET'])
def get_user_info(userID):
    """Get detailed info for a specific user
    ---
    parameters:
        - name: id
          in: query
          type: string
          required: true
    """

    # try:
    #     user = UserExample.objects(_id=ObjectId(userID)).first()
    #     if not user:
    #         abort(400)

    #     user_events = ErrorExample.objects(user=ObjectId(userID))
    #     return jsonify({'user': user, 'events': user_events})
    # except Exception as e:
    #     print(e)
    #     abort(400)

    if not userID:
        return jsonify({'data': 'User ID needed', 'status': False, 'code': 401})
    
    try:
        user = User.objects(_id=ObjectId(userID)).first()

        if not user:
            return jsonify({'data': 'User not found', 'status': False, 'code': 402})

        user_events = ErrorData.objects(user=ObjectId(userID))

        user_info = user.to_dict()
        user_info['events'] = [event.to_dict(withUserInfo=False) for event in user_events]

        return jsonify({'data': user_info, 'status': True, 'code': 200})

    except bsonError.InvalidId:
        return jsonify({'data': 'User ID not valid', 'status': False, 'code': 401})
