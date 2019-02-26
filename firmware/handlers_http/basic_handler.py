from tornado.web import RequestHandler
from printcore_modified import gcoder
import pickle
import tornado

class BasicHandler(RequestHandler):

    OFFSET_PATH = "/home/pi/config-files/offsets.json"
    
    def prepare(self):
        self.firmware = self.application.firmware
        self.print_finished_controller = self.application.print_finished_controller

    def get_user_locale(self):
        #TODO: sacar de un json
        return tornado.locale.get("en_US")