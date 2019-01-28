from handlers_http.basic_handler import BasicHandler
from tornado.options import options

class SetupHandler(BasicHandler):
    def get(self):
        self.render("setup.html")

class FilamentsHandler(BasicHandler):
    def get(self):
        action = self.request.path.split("/")[1]
        if action == "load":
            self.firmware.load_filament()
        elif action == "unload":
            self.firmware.unload_filament()
        self.render("filament_action.html", action=action)

class ToFilamentsHandler(BasicHandler):
    def get(self):
        self.render("filaments_selection.html")