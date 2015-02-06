from flask import Flask
from flask.ext import restful
from bson import json_util
import genetic

app = Flask(__name__)
api = restful.Api(app)

from parse_rest.connection import register
register("To6ZjPMq8BUtsCyUDGHSG8BtwVfSpNJ3XjpxdMOh", "g90vPDRIVQZp1Pc8VlaC8ekEH3rTDvY4vXHuFbGF", master_key = "PD2mJf48vAaItVo5NdCWYeuCArAPgOsoOHWY4s6V")

from parse_rest.datatypes import Object

class Crop(Object):
    pass

class Magic(restful.Resource):
    def get(self, soil, size):
        if soil and size:
            print size
            print soil
            crops = Crop.Query.filter(soil=soil)
            results = genetic.gen(crops, size, soil)
            return json_util.dumps(results)

api.add_resource(Magic, '/magic/<string:soil>/<string:size>')

if __name__ == '__main__':
    app.run(debug=True)