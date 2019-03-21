from tornado.web import RequestHandler
from printcore_modified import gcoder
import pickle
import tornado

class BasicHandler(RequestHandler):

    OFFSET_PATH = "/home/pi/config-files/offsets.json"
    
    def prepare(self):
        self.firmware = self.application.firmware
        self.wizzard = self.application.wizzard

    def get_user_locale(self):
        return tornado.locale.get(self.firmware.user_conf_json["language"])