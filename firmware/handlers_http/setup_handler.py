from handlers_http.basic_handler import BasicHandler
from tornado.options import options
from utils import get_extruder_materials, get_volume, set_volume
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
        self.render("filaments_type.html", ext_action=action, ext_type=extruder, mat_temps=get_extruder_materials())

class LoadUnloadFilamentsHandler(BasicHandler):
    def get(self, filament_type):
        extruder = self.request.path.split("/")[1]
        action = self.request.path.split("/")[2]
        material = get_extruder_materials()[filament_type]
        if action == "load":
            self.firmware.start_load_filament(extruder)
            action = "filament_auto_load"
        elif action == "unload":
            self.firmware.start_unload_filament(extruder)
            action = "filament_auto_unload"
        self.render("filament_action.html", action=action, material=material, ext_type=extruder)

class MaintainTempHandler(BasicHandler):
    def post(self):
        self.firmware.maintain_temperature(self.get_body_argument("target"))
        self.write("ok")

class ExtrudeHandler(BasicHandler):
    def get(self):
        self.firmware.extrude_filament()
        self.write("ok")

class ExtrudeOneMoreHandler(BasicHandler):
    def get(self):
        self.firmware.extrude_one_more()
        self.write("ok")

class RetractHandler(BasicHandler):
    def get(self):
        self.firmware.retract_filament()
        self.write("ok")

class ToFilamentsHandler(BasicHandler):
    def get(self):
        self.render("filaments_selection.html", wizzard_viewed=self.wizzard.viewed)

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
        self.render("updates.html", wizzard_viewed=self.wizzard.viewed)

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

class ToSoundHandler(BasicHandler):
    def get(self):
        self.render("sound.html", volume=get_volume())
    
    def post(self):
        volume = self.get_body_argument("volume")
        set_volume(volume)
        self.write(str(get_volume()))

class TurnOffMotorsHandler(BasicHandler):
    def get(self):
        self.firmware.turn_off_motors()
        self.write("ok")

class TurnOnMotorsHandler(BasicHandler):
    def get(self):
        self.firmware.turn_on_motors()
        self.write("ok")

class NozzlesHandler(BasicHandler):
    def get(self):
        nozzle_1 = self.firmware.user_conf_json["nozzle_1"]
        nozzle_2 = self.firmware.user_conf_json["nozzle_2"]
        self.render("nozzles.html", nozzle_1=nozzle_1, nozzle_2=nozzle_2)

class NozzleChangeHandler(BasicHandler):
    def get(self, nozzle):
        nozzle = self.get_body_argument("nozzle")
        size = self.get_body_argument("size")
        self.firmware.set_nozzle_size(nozzle, size)
        self.firmware.write_user_conf()
        self.write("ok")

class NozzlesSetHandler(BasicHandler):
    def get(self):
        nozzle_1 = self.firmware.user_conf_json["nozzle_1"]
        nozzle_2 = self.firmware.user_conf_json["nozzle_2"]
        self.render("nozzles.html", nozzle_1=nozzle_1, nozzle_2=nozzle_2)

class LanguageHandler(BasicHandler):
    def get(self):
        self.render("language.html", lang=self.firmware.user_conf_json["language"], wizzard_viewed=self.wizzard.viewed)

    def post(self):
        language = self.get_body_argument("language")
        self.firmware.set_language(language)
        self.write("ok")

class UpdateWarningHandler(BasicHandler):
    def get(self):
        self.render("update_warning.html", next_page=self.wizzard.give_me_page())

class NextWizzardHandler(BasicHandler):
    def get(self):
        self.redirect(self.wizzard.give_me_page())