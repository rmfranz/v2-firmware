from tornado.web import RequestHandler
from printcore_modified import gcoder
import pickle
import tornado
from tornado import concurrent

class BasicHandler(RequestHandler):

    OFFSET_PATH = "/home/pi/config-files/offsets.json"
    executor = concurrent.futures.ThreadPoolExecutor(5)
    
    def prepare(self):
        self.firmware = self.application.firmware
        self.wizzard = self.application.wizzard
        self.app_logger = self.application.app_logger

    def get_user_locale(self):
        return tornado.locale.get(self.firmware.user_conf_json["language"])

    def write_error(self, status_code, **kwargs):
        self.render("error.html")