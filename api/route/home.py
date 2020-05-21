from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from api.model.welcome import WelcomeModel
from api.schema.welcome import WelcomeSchema

home_api = Blueprint('api', __name__)


@home_api.route('/', defaults={'page': 'index'})
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Welcome to the Flask Starter Kit',
            'schema': WelcomeSchema
        }
    }
})
def welcome(page):
    result = WelcomeModel()
    return WelcomeSchema().dump(result), 200
