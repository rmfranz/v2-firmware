from tornado.web import RequestHandler
from printcore_modified import gcoder
import pickle

class BasicHandler(RequestHandler):

    def prepare(self):
        self.firmware = self.application.firmware