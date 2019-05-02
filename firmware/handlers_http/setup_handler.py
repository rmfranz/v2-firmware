from handlers_http.basic_handler import BasicHandler
from tornado.options import options
from utils import get_extruder_materials, get_volume, set_volume, restore_user_pref, reset_mac, check_connectivity
import os
import json
from subprocess import check_output


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
        if os.path.exists("/home/pi/dev_mode"):
            self.render("updates_dev.html", wizzard_viewed=self.wizzard.viewed)
        else:
            self.render("updates.html", wizzard_viewed=self.wizzard.viewed)

class GetUpdateHandler(BasicHandler):
    def get(self):
        new = check_output("(git fetch --tags origin && git tag) | grep '[0-9]\+.[0-9]\+.[0-9]\+' | tail -1", shell=True, universal_newlines=True)
        try:
            actual = check_output("git describe --abbrev=0", shell=True, universal_newlines=True)
        except:
            actual = "0"
        self.write({"new": new, "actual": actual, "connectivity": check_connectivity()})

class GetActualVersionHandler(BasicHandler):
    def get(self):
        try:
            actual = check_output("git describe --abbrev=0", shell=True, universal_newlines=True)
        except:
            actual = "0"
        self.write({"actual": actual})

class GetUpdateToDevHandler(BasicHandler):
    def get(self):
        scanoutput = check_output("git fetch --tags origin && git tag", shell=True, universal_newlines=True)
        tags = [n for n in scanoutput.split("\n") if n and n != "vinicial"]
        tags.append("master")
        tags.sort(reverse = True)
        self.write({"tags": tags[:5]})

    def post(self):
        version = self.get_body_argument("version")
        scanoutput = check_output("git fetch --tags origin && git tag", shell=True, universal_newlines=True)
        tags = [n for n in scanoutput.split("\n") if n and n != "vinicial"]
        tags.append("master")
        if version in tags:
            if version == "master":
                os.system("git checkout -f")
                os.system("git checkout master")
                os.system("git fetch")
                os.system("git pull")
            else:
                os.system("git checkout -f")
                os.system("git fetch")
                os.system("git checkout {}".format(version))
            os.system("sudo killall pigpiod")
            os.system("sudo reboot -h now")
            self.write("ok")
        else:
            self.redirect("/software-update")

class UpdateHandler(BasicHandler):
    def get(self):
        new = check_output("(git fetch --tags origin && git tag) | grep '[0-9]\+.[0-9]\+.[0-9]\+' | tail -1", shell=True, universal_newlines=True)
        os.system("git checkout -f")
        os.system("git fetch")
        os.system("git checkout {}".format(new))
        if self.application.gpio.is_initialized:
            self.application.gpio.stop()
        os.system("sudo killall pigpiod")
        os.system("sudo reboot -h now")
        self.write("ok")

class ToInfoHandler(BasicHandler):
    def get(self):
        self.render("info.html", serial=self.firmware.get_serial_number(), mac_address=self.firmware.get_macaddress(), hard_version=self.firmware.hardware_json["hw_version"])

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
        size = self.get_argument('size', "0.4")
        self.render("nozzle_sizes.html", nozzle=nozzle, size=size)

class NozzlesSetHandler(BasicHandler):
    def post(self):
        nozzle = self.get_body_argument("nozzle")
        size = self.get_body_argument("size")
        self.firmware.set_nozzle_size(nozzle, size)
        self.firmware.write_user_conf()
        self.write("ok")

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

class EnableDebModeHandler(BasicHandler):
    def get(self):
        os.system("touch /home/pi/dev_mode")
        self.write("ok")

    def post(self):
        password = self.get_body_argument("password", default="")
        if password == "kOdak.dEv":
            self.render("dev_mode.html")
        else:
            self.redirect("/home")

class DisableDebModeHandler(BasicHandler):
    def get(self):
        if os.path.exists("/home/pi/dev_mode"):
            os.system("sudo rm /home/pi/dev_mode")
        self.redirect("/home")

class ResetBoardUuidHandler(BasicHandler):
    def get(self):
        board_info = self.firmware.get_board_info()
        if not board_info:
            self.write("01")
        elif len(board_info) > 1:
            self.write("02")
        else:
            self.firmware.set_board_info(board_info[0].split()[8])
            self.write("ok")

class ToSkipWizardHandler(BasicHandler):
    def get(self):
        self.render("skip_wizard.html")

class SkipWizardHandler(BasicHandler):
    def get(self):
        self.wizzard.skip_me()
        self.redirect("/home")

class RestoreUserPref(BasicHandler):
    def get(self):
        restore_user_pref()
        self.write("ok")

class ResetMacPref(BasicHandler):
    def get(self):
        reset_mac()
        self.write("ok")

class SetConnectionStatusHandler(BasicHandler):
    def get(self):
        with open("/home/pi/config-files/user_conf.json") as f:
            user_conf_json = json.load(f)
        result = str(check_connectivity())
        self.set_cookie('cloud_status', user_conf_json['cloud_pref'])
        self.set_cookie('wifi_status', result)
        self.write({'cloud_status': user_conf_json['cloud_pref'], 'wifi_status': result})