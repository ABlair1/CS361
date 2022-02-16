# Author: Andrew Blair
# Date: 2/10/2022
# Description: 

from flask import Flask
from flask_restful import Api, Resource
import json
from .kg_converter import convert_to_kgs, convert_from_kgs

app = Flask(__name__)
api = Api(app)

class MassConverter(Resource):
    """###"""
    def post(self):
        """###"""
        req_params = {}
        # business logic for getting input/parameters from post request
        # call conversion functions as necessary 
        # return result in json format 
        
# Register GhgData resource with API at root endpoint
api.add_resource(MassConverter, '/')

if __name__ == "__main__":
    app.run(debug=True)