from tornado.web import RequestHandler
from printcore_modified import gcoder
import pickle

class BasicHandler(RequestHandler):

    OFFSET_PATH = "/home/pi/config-files/offsets.json"
    
    def prepare(self):
        self.firmware = self.application.firmware