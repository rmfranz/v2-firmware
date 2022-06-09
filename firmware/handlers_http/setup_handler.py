from handlers_http.basic_handler import BasicHandler
from tornado.options import options
from utils import get_extruder_materials, get_volume, set_volume, restore_user_pref, reset_mac, check_connectivity, mount_usb, reset_rpi, get_logs
import os
import json
from subprocess import check_output
from tornado import httpclient, concurrent, gen
import traceback
from distutils import dir_util

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
        self.render("filaments_type.html", ext_action=action, ext_type=extruder, mat_temps=get_extruder_materials(self.firmware.filaments_json))

class LoadUnloadFilamentsHandler(BasicHandler):
    def get(self):
        filament_type = self.get_argument('material')
        extruder = self.request.path.split("/")[1]
        action = self.request.path.split("/")[2]
        material = get_extruder_materials(self.firmware.filaments_json)[filament_type]['name']
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

class RetractOneMoreHandler(BasicHandler):
    def get(self):
        self.firmware.retract_one_more()
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

class ToUpdateSelectionHandler(BasicHandler):
    def get(self):
        self.render("update_selection.html")

class ToUsbUpdateHandler(BasicHandler):
    def get(self):
        self.render("update_usb.html")

class UsbUpdate(BasicHandler):
    def get(self):
        result = mount_usb(self.firmware.hardware_json["board_uuid"])
        if result == 0:
            md5 = os.system('cd /media/usb && md5sum -c firmware.zip.md5')
            if md5 != 0:
                self.app_logger.error('USB update error: error with md5')
                self.write({'error': 3})
            else:
                step1 = os.system('sudo cp /media/usb/firmware.zip /home/pi && sudo sync')
                step2 = os.system('sudo unzip -P kOdak..fIrmw2019?? /home/pi/firmware.zip -d /home/pi/firmware_unziped')
                if step1 == 0 and step2 == 0:
                    #result = os.system('sudo rsync /home/pi/firmware_unziped/ /home/pi/v2-firmware')
                    try:
                        dir_util.copy_tree('/home/pi/firmware_unziped', '/home/pi/v2-firmware')
                        os.system("sudo chown -R pi:pi /home/pi/v2-firmware")
                        os.system('sudo rm -r /home/pi/firmware_unziped')
                        os.system('sudo touch /home/pi/usb_updated')
                        reset_rpi()
                        self.write("ok")
                    except:
                        self.app_logger.error('USB update error: error copying files')
                        self.write({'error': 5})
                else:
                    self.app_logger.error('USB update error: error copying or unzipping zip file')
                    self.write({'error': 4})
        elif result == 1:
            self.app_logger.error('USB update error: error mounting usb')
            self.write({'error': 1})
        else:
            self.app_logger.error('USB update error: error {}'.format(str(result)))
            self.write({'error': 2})
        

class ToUpdateHandler(BasicHandler):
    def get(self):
        if os.path.exists("/home/pi/dev_mode"):
            hash = check_output("sudo git rev-parse --short HEAD", shell=True, universal_newlines=True)
            self.render("updates_dev.html", wizzard_viewed=self.wizzard.viewed, version=hash)
        else:
            self.render("updates.html", wizzard_viewed=self.wizzard.viewed)

class GetUpdateHandler(BasicHandler):
    @gen.coroutine
    def get(self):
        error = None
        new = yield self.get_new_tag()
        try:
            actual = check_output("sudo git describe --abbrev=0", shell=True, universal_newlines=True)
        except Exception:
            self.app_logger.error('Get update error: error getting actual version {}'.format(str(traceback.format_exc())))
            actual = "0"
        if not new:
            error = "error"
        self.write({"new": new, "actual": actual, "connectivity": check_connectivity(), 'error': error})

    @concurrent.run_on_executor
    def get_new_tag(self):
        try:
            new_tag = check_output("sudo git fetch --tags origin && git tag | grep '[0-9]\+.[0-9]\+.[0-9]\+' | tail -1",
                    shell=True, universal_newlines=True)
        except Exception:
            self.app_logger.error('Get update error: error getting tags {}'.format(str(traceback.format_exc())))
            new_tag = None
        return new_tag
        

class GetActualVersionHandler(BasicHandler):
    def get(self):
        try:
            actual = check_output("sudo git describe --abbrev=0", shell=True, universal_newlines=True)
        except Exception:
            self.app_logger.error('Get update error: error getting actual version {}'.format(str(traceback.format_exc())))
            actual = "0"
        self.write({"actual": actual})

class GetUpdateToDevHandler(BasicHandler):
    @gen.coroutine
    def get(self):
        scanoutput = yield self.get_tags()
        tags = [n for n in scanoutput.split("\n") if n and n != "vinicial"]
        tags.append("master")
        tags.sort(reverse = True)
        self.write({"tags": tags[:5]})

    @concurrent.run_on_executor
    def get_tags(self):
        return check_output("sudo git fetch --tags origin && git tag", shell=True, universal_newlines=True)

    def post(self):
        version = self.get_body_argument("version")
        scanoutput = check_output("sudo git fetch --tags origin && git tag", shell=True, universal_newlines=True)
        tags = [n for n in scanoutput.split("\n") if n and n != "vinicial"]
        tags.append("master")
        os.system("sudo git checkout -f")
        os.system("sudo git fetch --all")
        os.system("sudo git reset --hard origin/master")
        if version == "master":
            os.system("sudo git checkout master")
            os.system("sudo git pull")
        else:
            os.system("sudo git checkout {}".format(version))
            os.system("sudo git pull origin {}".format(version))
        reset_rpi()
        self.write("ok")

class UpdateHandler(BasicHandler):
    def get(self):
        new = check_output("(sudo git fetch --tags origin && git tag) | grep '[0-9]\+.[0-9]\+.[0-9]\+' | tail -1", shell=True, universal_newlines=True)
        os.system("sudo git checkout -f")
        os.system("sudo git fetch --all")
        os.system("sudo git reset --hard origin/master")
        os.system("sudo git checkout {}".format(new))
        if self.application.gpio.is_initialized:
            self.application.gpio.stop()
        reset_rpi()
        self.write("ok")

class RepairUpdateHandler(BasicHandler):
    def get(self):
        '''
        Source http://vincesalvino.blogspot.com/2013/08/git-empty-files-corrupt-objects-and.html
        '''
        rm = os.system('find .git/objects/ -size 0 -exec rm -f {} \;')
        if rm == 0:
            try:
                new = check_output("(sudo git fetch --tags origin && git tag) | grep '[0-9]\+.[0-9]\+.[0-9]\+' | tail -1", shell=True, universal_newlines=True)
                os.system("sudo git checkout -f")
                os.system("sudo git fetch --all")
                os.system("sudo git reset --hard origin/master")
                os.system("sudo git clean -f")
                os.system("sudo git checkout {}".format(new))
                if self.application.gpio.is_initialized:
                    self.application.gpio.stop()
                reset_rpi()
                self.write('ok')
            except Exception:
                self.app_logger.error('Repair update error: error repairing update {}'.format(str(traceback.format_exc())))
                self.write('error')
        else:
            self.app_logger.error('Repair update error: error removing corrupt objects')
            self.write('error')

class ToInfoHandler(BasicHandler):
    def get(self):
        mac_address = self.firmware.get_macaddress().upper()
        token = mac_address.replace(':', '')[6:]
        self.render("info.html", serial=self.firmware.get_serial_number(), mac_address=mac_address, 
            hard_version=self.firmware.hardware_json["hw_version"], token=token)

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
        async_http_client = httpclient.AsyncHTTPClient()
        async_http_client.fetch("http://127.0.0.1:9000/refresh", raise_error=False)
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

class ToUserDevModeHandler(BasicHandler):
    def get(self):
        self.render("user_dev_mode.html")

class EnableDevModeHandler(BasicHandler):
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
            self.app_logger.error('Reset board error: no board info')
            self.write("01")
        elif len(board_info) > 1:
            self.app_logger.error('Reset board error: More than one board detected. USB connected?')
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
    @gen.coroutine
    def get(self):
        with open("/home/pi/config-files/user_conf.json") as f:
            user_conf_json = json.load(f)
        result = "no-connected"
        try:
            result = yield self.get_connectivity()
        except Exception:
            self.app_logger.error('Set connection error: could not get connectivity with this error: {}'.format(str(traceback.format_exc())))
        self.set_cookie('cloud_status', user_conf_json['cloud_pref'])
        self.set_cookie('wifi_status', result)
        self.write({'cloud_status': user_conf_json['cloud_pref'], 'wifi_status': result})

    @concurrent.run_on_executor
    def get_connectivity(self):
        return str(check_connectivity().split("\n")[0])

class ToggleDebugHandler(BasicHandler):
    def get(self):
        debug = self.get_argument('debug')
        if debug == 'enable':
            os.system('sudo touch /home/pi/enable_debug && chown pi:pi /home/pi/enable_debug')
        elif debug == 'disable':
            os.system('sudo rm /home/pi/enable_debug')
        self.write('ok')

class GetLogsHandler(BasicHandler):
    def get(self):
        result = mount_usb(self.firmware.hardware_json["board_uuid"])
        if result == 0:
            get_logs()
            self.write('ok')
        else:
            self.write('error')

class UpdateBoarConfig(BasicHandler):
    def get(self):
        result = self.firmware.put_config()
        self.write({'error': result})