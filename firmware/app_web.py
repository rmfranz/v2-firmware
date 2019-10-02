import tornado.web
import tornado.websocket
from printcore_modified.printcore import printcore
from tornado.options import parse_command_line
from tornado.options import define, options
from handlers_http.print_handler import * 
from handlers_http.basic_handler import * 
from handlers_http.calibration_handler import *
from handlers_http.back_handler import *
from handlers_http.connection_handler import *
from handlers_websocket.temperatures_ws_handler import *
from handlers_websocket.calibration_ws_handler import *
from handlers_websocket.print_ws_handler import *
from handlers_websocket.cloud_ws_handler import *
from handlers_websocket.error_ws_handler import *
from handlers_http.setup_handler import *
from handlers_http.build_plate_handler import *
from handlers_http.lights_handler import *
from handlers_http.extruders_handler import *
from handlers_http.network_handler import *
from handlers_http.cloud_handler import *
from firmware.director import FirmwareDirector
from tornado import httpclient
import logging
import pickle
import os
from firmware.gpio import Gpio
from firmware.wizzard import Wizzard
from utils import check_file_print_finished, perform_os_check, check_premature_os, delete_corrupt, enable_loggers
from tornado.ioloop import PeriodicCallback
import json

define("template_folder", default="templates/", help="Folder to use")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/home", HomeHandler),
            (r"/check-update", CheckUpdateHandler),
            (r"/update-board-config", CheckUpdateHandler),
            (r"/set-board-uuid", SetBoardUuidHandler),
            (r"/setup", SetupHandler),
            (r"/advanced", AdvancedHandler),
            (r"/basic", ToBasicHandler),
            (r"/to-cloud", ToCloudHandler),
            (r"/get-cloud-token", GetRegistrationCodeHandler),
            (r"/cloud-unregister", UnregisterHandler),
            (r"/cloud-disconnect", DisconnectHandler),
            (r"/cloud-reconnect", ReconnectHandler),
            (r"/to-cloud-queue", ToQueueHandler),
            (r"/get-cloud-queue", GetQueueHandler),
            (r"/confirm-cloud-print", ToConfirmPrintHandler),
            (r"/print-cloud", PrintCloudHandler),
            (r"/set-user-cloud-pref", SetUserCloudHanlder),
            (r"/get-update", GetUpdateHandler),
            (r"/get-actual-version", GetActualVersionHandler),
            (r"/get-dev-update", GetUpdateToDevHandler),
            (r"/software-update", ToUpdateSelectionHandler),
            (r"/repair-update", RepairUpdateHandler),
            (r"/internet-update", ToUpdateHandler),
            (r"/usb-update", ToUsbUpdateHandler),
            (r"/make-usb-update", UsbUpdate),
            (r"/make-update", UpdateHandler),
            (r"/manual-controls", ToManualControlHandler),
            (r"/back-manual-controls", BackPlateHandler),
            (r"/build-plate-controls", ToBuildPlateControlHandler),
            (r"/homming", HomeHandler),
            (r"/plate-up", PlateUpHandler),
            (r"/plate-down", PlateDownHandler),
            (r"/plate-home", PlateHomeHandler),
            (r"/bed-temp/([0-9]+)", PlateTemperatureHandler),
            (r"/plate-select-temp", ToPlateTemperatureHandler),
            (r"/extruders-controls", ToExtrudersControlHandler),
            (r"/get-extruder-options", GetExtrudersControlHandler),
            (r"/back-extruder", BackExtruderHandler),
            (r"/ext_1", ToExtruderTemperatureHandler),
            (r"/ext_2", ToExtruderTemperatureHandler),
            (r"/ext_1/extrude", ExtruderActionHandler),
            (r"/ext_1/retract", ExtruderActionHandler),
            (r"/ext_2/extrude", ExtruderActionHandler),
            (r"/ext_2/retract", ExtruderActionHandler),
            (r"/ext_1/([0-9]+)", ExtruderTemperatureHandler),
            (r"/ext_2/([0-9]+)", ExtruderTemperatureHandler),
            (r"/print", PrintHandler),
            (r"/print-now", PrintNowHandler),
            (r"/test-print", TestHandler),
            (r"/pausa", PauseHandler),
            (r"/resume", ResumeHandler),
            (r"/cancelar", CancelHandler),
            (r"/cancel-cloud", CancelCloudHandler),
            (r"/print-end", PrintFinishedHandler),
            (r"/print-end-back", BackPrintFinishedHandler),
            (r"/print-total-lines", GetTotalLinesHandler),
            (r"/print-selection", PrintSelectionHandler),
            (r"/get-percentage", GetPercentage),
            (r"/get-line-num", GetNumLineHandler),
            (r"/get-temperatures", TemperaturesHandler),
            (r"/local-files-selection", LocalFilesSelectionHandler),
            (r"/listing-files/([0-9]+)", ListingFilesHandler),
            (r"/listing-files/usb", ListingUsbHandler),
            (r"/confirm-print", PreviousPrintHandler),
            (r"/violent-pause", ViolentPauseHandler),
            (r"/put-serial", SerialHandler),
            (r"/put-version", VersionHandler),
            (r"/select-calibration", CalibrationHandler),
            (r"/back-calibration-selection", BackSelectCalibrationHandler),
            (r"/get-offsets", GetOffsetsHandler),
            (r"/t0-calibration", ZOffsetT0CalibrationHandler),
            (r"/t1-calibration", ZOffsetT1CalibrationHandler),
            (r"/z-offset-up", UpZOffsetCalibrationHandler),
            (r"/z-offset-down", DownZOffsetCalibrationHandler),
            (r"/build-plate-calibration", BuildPlateCalibrationHandler),
            (r"/z-offset-calibration", ZOffsetCalibrationHandler),
            (r"/xy-offset-calibration", XYOffsetCalibrationHandler),
            (r"/points-25-calibration", Points25Calibration),
            (r"/save-25-calibration", SavePoints25Calibration),
            (r"/make-3-calibration", Points3Calibration),
            (r"/show-grid", Show25GridCalibration),
            (r"/reset-grid", ResetGridCalibration),
            (r"/wifi-connection", ToWifiConnectionHandler),
            (r"/get-wifi-connection", WifiConnectionHandler),
            (r"/activate-wifi", EnableWifiHandler),
            (r"/deactivate-wifi", DisableWifiHandler),
            (r"/forget-wifi", ForgetNetworkHandler),
            (r"/load", ToFilamentsExtrudersHandler),
            (r"/unload", ToFilamentsExtrudersHandler),
            (r"/filaments-selection", ToFilamentsHandler),
            (r"/ext_1/load", FilamentsHandler),
            (r"/ext_1/unload", FilamentsHandler),
            (r"/ext_2/load", FilamentsHandler),
            (r"/ext_2/unload", FilamentsHandler),
            (r"/ext_1/load/action", LoadUnloadFilamentsHandler),
            (r"/ext_1/unload/action", LoadUnloadFilamentsHandler),
            (r"/ext_2/load/action", LoadUnloadFilamentsHandler),
            (r"/ext_2/unload/action", LoadUnloadFilamentsHandler),
            (r"/maintain-temp", MaintainTempHandler),
            (r"/extrude", ExtrudeHandler),
            (r"/retract", RetractHandler),
            (r"/extrude-more", ExtrudeOneMoreHandler),
            (r"/retract-more", RetractOneMoreHandler),
            (r"/back-load-unload", BackLoadUnloadActionHandler),
            (r"/back-filaments-selection", BackLoadUnloadHandler),
            (r"/connectivity", ConnectivityHandler),
            (r"/network-info", ToNetworkInfoHandler),
            (r"/info", ToInfoHandler),
            (r"/sound", ToSoundHandler),
            (r"/ssh-enable", EnableSSHHandler),
            (r"/ssh-disable", DisableSSHHandler),
            (r"/enable-dev-mode", EnableDebModeHandler),
            (r"/disable-dev-mode", DisableDebModeHandler),
            (r"/dev-mode", ToUserDevModeHandler),
            (r"/lights", ToLightsHandler),
            (r"/lights/red", LightsHandler),
            (r"/lights/green", LightsHandler),
            (r"/lights/blue", LightsHandler),
            (r"/lights/other", LightsHandler),
            (r"/lights/light_blue", LightsHandler),
            (r"/lights/orange", LightsHandler),
            (r"/lights/white", LightsHandler),
            (r"/lights/off", LightsHandler),
            (r"/turn-off-motors", TurnOffMotorsHandler),
            (r"/turn-on-motors", TurnOnMotorsHandler),
            (r"/nozzles", NozzlesHandler),
            (r"/nozzle/([0-9]+)", NozzleChangeHandler),
            (r"/set-nozzle", NozzlesSetHandler),
            (r"/language", LanguageHandler),
            (r"/update-warning", UpdateWarningHandler),
            (r"/next-wizzard", NextWizzardHandler),
            (r"/to-skip", ToSkipWizardHandler),
            (r"/skip-wizard", SkipWizardHandler),
            (r"/reset-board-uuid", ResetBoardUuidHandler),
            (r"/restore-user-pref", RestoreUserPref),
            (r"/reset-mac", ResetMacPref),
            (r"/toggle-debug", ToggleDebugHandler),
            (r"/get-log", GetLogsHandler),
            (r"/set_connection_status", SetConnectionStatusHandler),
            (r"/temperatures", TemperaturesWsHandler),
            (r"/heating-bed", HeatingBedWsHandler),
            (r"/heating-nozzle", HeatingNozzleWsHandler),
            (r"/probe-complete", ProbeCompleteWsHandler),
            (r"/probe-failed", ProbeFailedWsHandler),
            (r"/grid-saved", GridSavedWsHandler),
            (r"/z-probe", ZProbeWsHandler),
            (r"/inspect-grid", InspectGridWsHandler),
            (r"/waiting-file", WaitingFileWsHandler),
            (r"/print-finished", PrintFinishedWsHandler),
            (r"/cloud", CloudWsHandler),
            (r"/error-handler", ErrorWsHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "/home/pi/v2-firmware/firmware/assets"}),
            (r'/print_images/(.*)', tornado.web.StaticFileHandler, {'path': "/home/pi/print_images"}),
            (r'/sample_images/(.*)', tornado.web.StaticFileHandler, {'path': "/home/pi/v2-firmware/Samples"}),
            (r'/calib_images/(.*)', tornado.web.StaticFileHandler, {'path': "/home/pi/v2-firmware/calibrationObjects"}),
        ]
        #tornado.web.Application.__init__(self, handlers, template_path="/home/pi/v2-firmware/firmware/templates/", autoreload=True,
        #    compiled_template_cache=False, static_hash_cache=False)
        tornado.web.Application.__init__(self, handlers, template_path="/home/pi/v2-firmware/firmware/templates/")
        perform_os_check()
        #check_premature_os()
        #Put FirmwareDirector, this is wrong
        self.firmware = FirmwareDirector().give_me_firmware()
        self.gpio = Gpio()
        self.wizzard = Wizzard()
        self.app_logger = logging.getLogger('app_logger')
        self.violent_caller = PeriodicCallback(self.violent_call, 3600000)
        self.violent_counter = 0

    def violent_call(self):
        self.violent_counter = self.violent_counter + 1
        result = self.violent_counter % 10
        if result == 0:
            async_http_client = httpclient.AsyncHTTPClient()
            async_http_client.fetch("http://127.0.0.1:8888/violent-pause")

    def counter_to_zero(self):
        self.violent_counter = 0

class HomeHandler(BasicHandler):
    def get(self):
        skipp = int(self.get_argument("wizzard", 1))
        if skipp == 0 and not self.wizzard.viewed:
            self.wizzard.viewed = True
        async_http_client = httpclient.AsyncHTTPClient()
        async_http_client.fetch("http://127.0.0.1:9000/init-websockets")
        if os.path.exists("/home/pi/print_images/print.png"):
            os.remove("/home/pi/print_images/print.png")
        if not self.application.gpio.is_initialized:
            self.application.gpio.initialize()
        if not self.firmware.check_mac_address():
            delete_corrupt()
            board_info = self.firmware.get_board_info()
            if not board_info :
                self.render("put_serial.html", error=0)
            elif len(board_info) > 1:
                self.render("put_serial.html", error=1)
            else:
                self.firmware.set_board_info(board_info[0].split()[8])
                self.render("put_serial.html", error=None)
        elif not self.firmware.check_serial():
            delete_corrupt()
            self.render("put_serial.html", error=None)
        elif not self.firmware.check_version():
            delete_corrupt()
            self.render("put_version.html", version_list=self.firmware.get_version_list())
        elif not self.firmware.is_initialized:
            self.firmware.initialize()
            delete_corrupt()
            if self.wizzard.viewed:
                self.render("index.html")
            else:
                self.redirect(self.wizzard.give_me_page())
        else:
            delete_corrupt()
            if self.wizzard.viewed:
                self.render("index.html")
            else:
                self.redirect(self.wizzard.give_me_page())

class SerialHandler(BasicHandler):
    def post(self):
        serial = self.get_body_argument("serial")
        self.firmware.set_serial(serial)
        #async_http_client = httpclient.AsyncHTTPClient()
        #async_http_client.fetch("http://127.0.0.1:9000/set-serial", method='POST', raise_error=False,
        #    headers={'Content-Type': 'application/json'}, 
        #    body=json.dumps({"serial": serial}))
        #self.firmware.put_config()
        self.render("put_version.html", version_list=self.firmware.get_version_list())

class VersionHandler(BasicHandler):
    def post(self):
        version = self.get_body_argument("version")
        self.firmware.set_version(version)
        self.application.firmware = FirmwareDirector().give_me_firmware()
        self.application.firmware.initialize()
        async_http_client = httpclient.AsyncHTTPClient()
        async_http_client.fetch("http://127.0.0.1:9000/refresh", raise_error=False)
        self.redirect("/home")

class CheckUpdateHandler(BasicHandler):
    def get(self):
        self.write({"result": os.path.exists("/home/pi/config_updted")})

if __name__ == "__main__":
    if os.path.exists("/home/pi/enable_debug"):
        enable_loggers()
    app = Application()
    parse_command_line()
    tornado.locale.load_translations("/home/pi/v2-firmware/translations")
    app.listen(8888)
    try:
        logging.info('Starting app')
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('Exit success')