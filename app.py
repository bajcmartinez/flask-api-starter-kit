from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from api.route.api import api
from api.model.models import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['SWAGGER'] = {
        'title': 'Flask API Starter Kit',
    }
    Swagger(app)

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    app.config.from_pyfile('config.py')
    db.init_app(app)

    app.register_blueprint(api, url_prefix='/api')

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5100,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
