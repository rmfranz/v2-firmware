from handlers_http.basic_handler import BasicHandler
from tornado.options import options

class SetupHandler(BasicHandler):
    def get(self):
        self.render("setup.html")