from tornado.web import RequestHandler
from printcore_modified import gcoder
import pickle
import tornado

class BasicHandler(RequestHandler):

    OFFSET_PATH = "/home/pi/config-files/offsets.json"
    
    def prepare(self):
        self.firmware = self.application.firmware

    def get_user_locale(self):
        #TODO: sacar de un json
        return tornado.locale.get("en_US")