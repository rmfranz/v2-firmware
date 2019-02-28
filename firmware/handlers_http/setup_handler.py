from handlers_http.basic_handler import BasicHandler
from tornado.options import options
import os

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
        material = "PLAT"
        if action == "load":
            self.firmware.load_filament(extruder)
            action = "filament_auto_load"
        elif action == "unload":
            self.firmware.unload_filament(extruder)
            action = "filament_auto_unload"
        self.render("filament_action.html", action=action, material=material)

class ToFilamentsHandler(BasicHandler):
    def get(self):
        self.render("filaments_selection.html")

class ToManualControlHandler(BasicHandler):
    def get(self):
        lights_on = "true"
        if not self.application.gpio.lights_on:
            lights_on = "false"
        self.render("manual_ctl_select.html", lights_on=lights_on)

class SetBoardUuidHandler(BasicHandler):
    def get(self):
        if not self.firmware.hardware_json["board_uuid"]:
            self.firmware.set_board_info()
        self.write("ok")

class ToBasicHandler(BasicHandler):
    def get(self):
        self.render("basic.html")

class ToUpdateHandler(BasicHandler):
    def get(self):
        self.render("updates.html")

class UpdateHandler(BasicHandler):
    def get(self):
        os.system("git pull origin master")
        if self.application.gpio.is_initialized:
            self.application.gpio.stop()
        os.system("sudo killall pigpiod")
        os.system("sudo reboot -h now")
        self.write("ok")

class ToInfoHandler(BasicHandler):
    def get(self):
        self.render("info.html", serial=self.firmware.get_serial_number(), soft_version="V2", hard_version="V2")