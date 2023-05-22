from flask import Flask
from flask_restful import Resource, Api, reqparse

from gennifer_api import generateInputs, run, parseOutput


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('exp_dataset_uri')

class RunAlgo(Resource):
    def post(self):
        print("here")
        args = parser.parse_args()
        inputs = generateInputs(args['exp_dataset_uri'])
        print(inputs)
        res = run(inputs)
        output = parseOutput(res)
        return output, 201

api.add_resource(RunAlgo, '/run')

if __name__ == '__main__':
    app.run(debug=True)
