from handlers_http.basic_handler import BasicHandler
from tornado.options import options

class SetupHandler(BasicHandler):
    def get(self):
        self.render("setup.html")

class AdvancedHandler(BasicHandler):
    def get(self):
        self.render("advanced.html")

class ToFilamentsExtrudersHandler(BasicHandler):
    def get(self):
        self.render("filaments_extruders.html", action=self.request.path.split("/")[1])

class FilamentsHandler(BasicHandler):
    def get(self):
        extruder = self.request.path.split("/")[1]
        action = self.request.path.split("/")[2]
        self.render("filaments_type.html", ext_action=action, ext_type=extruder)

class LoadUnloadFilamentsHandler(BasicHandler):
    def get(self, filament_type):
        extruder = self.request.path.split("/")[1]
        action = self.request.path.split("/")[2]
        if action == "load":
            self.firmware.load_filament(extruder)
        elif action == "unload":
            self.firmware.unload_filament(extruder)
        self.render("filament_action.html", action=action)

class ToFilamentsHandler(BasicHandler):
    def get(self):
        self.render("filaments_selection.html")

class ToManualControlHandler(BasicHandler):
    def get(self):
        self.render("manual_ctl_select.html")

class SetBoardUuidHandler(BasicHandler):
    def get(self):
        if not self.firmware.hardware_json["board_uuid"]:
            self.firmware.set_board_info()
        self.write("ok")