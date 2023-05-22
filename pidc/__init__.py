import os
import requests_cache

from flask import Flask
from flask_restful import Resource, Api, reqparse

from .gennifer_api import generateInputs, run, parseOutput

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            )
    if test_config is None:
        # Load this instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the testing config if passed
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Install a requests cache
    requests_cache.install_cache('pidc_cache')
    
    # Build flask RESTful API
    api = Api(app)

    parser = reqparse.RequestParser()
    parser.add_argument('zenodo_id')

    class RunAlgo(Resource):
        def post(self):
            args = parser.parse_args()
            inputs = generateInputs(args['zenodo_id'])
            res = run(inputs)
            output = parseOutput(res)
            return output, 201

    api.add_resource(RunAlgo, '/run')

    return app
