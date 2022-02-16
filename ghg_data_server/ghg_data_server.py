# Author: Andrew Blair
# Date: 2/10/2022
# Description: 

from flask import Flask
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)
sourcePath = './ghg_data.json'

class GhgData(Resource):
    """Resource that can serve a greenhouse gas emissions data file."""
    def get(self):
        """Returns the contents of a JSON data file"""
        with open(sourcePath, 'r') as dataFile:
            data = json.load(dataFile)
        return data
        
# Register GhgData resource with API at root endpoint
api.add_resource(GhgData, '/')

if __name__ == "__main__":
    app.run(debug=True)