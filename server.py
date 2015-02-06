from twisted.web.server import Site       #import twisted stuff
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File
from bson import json_util
import genetic

from parse_rest.connection import register
register("To6ZjPMq8BUtsCyUDGHSG8BtwVfSpNJ3XjpxdMOh", "g90vPDRIVQZp1Pc8VlaC8ekEH3rTDvY4vXHuFbGF", master_key = "PD2mJf48vAaItVo5NdCWYeuCArAPgOsoOHWY4s6V")

from parse_rest.datatypes import Object

class Crop(Object):
    pass

class evaluateAPI(Resource):
  def render_GET(self, request):
      crops = Crop.Query.all()
      results = genetic.gen(crops)
      return json_util.dumps(results)

root = File("lampwww")               #Create a root
root.putChild("magic", evaluateAPI())     #Create a child that will handle requests (the second argument must be the class name)
factory = Site(root)             #Initialize the twisted object
reactor.listenTCP(8080, factory)   #Choose the port to listen on (80 is standard for HTTP)
                               #so don't bother putting anything after it

reactor.run()                         #Start listening, this command is an infinite loop