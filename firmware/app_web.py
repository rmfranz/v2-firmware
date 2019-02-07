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
from handlers_http.setup_handler import *
from handlers_http.build_plate_handler import *
from handlers_http.lights_handler import *
from handlers_http.extruders_handler import *
from handlers_http.network_handler import *
from firmware.smoothie_firmware import SmoothieFirmware
import logging
import pickle
import os
from firmware.gpio import Gpio

define("template_folder", default="templates/", help="Folder to use")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/home", HomeHandler),
            (r"/set-board-uuid", SetBoardUuidHandler),
            (r"/setup", SetupHandler),
            (r"/advanced", AdvancedHandler),
            (r"/basic", ToBasicHandler),
            (r"/software-update", ToUpdateHandler),
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
            (r"/pausa", PauseHandler),
            (r"/resume", ResumeHandler),
            (r"/cancelar", CancelHandler),
            (r"/get-temperatures", TemperaturesHandler),
            (r"/print-selection", PrintSelectionHandler),
            (r"/local-files-selection", LocalFilesSelectionHandler),
            (r"/listing-files/([0-9]+)", ListingFilesHandler),
            (r"/confirm-print", PreviousPrintHandler),
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
            (r"/show-grid", Show25GridCalibration),
            (r"/reset-grid", ResetGridCalibration),
            (r"/wifi-connection", WifiConnectionHandler),
            (r"/load", ToFilamentsExtrudersHandler),
            (r"/unload", ToFilamentsExtrudersHandler),
            (r"/filaments-selection", ToFilamentsHandler),
            (r"/ext_1/load", FilamentsHandler),
            (r"/ext_1/unload", FilamentsHandler),
            (r"/ext_2/load", FilamentsHandler),
            (r"/ext_2/unload", FilamentsHandler),
            (r"/ext_1/load/([0-9]+)", LoadUnloadFilamentsHandler),
            (r"/ext_1/unload/([0-9]+)", LoadUnloadFilamentsHandler),
            (r"/ext_2/load/([0-9]+)", LoadUnloadFilamentsHandler),
            (r"/ext_2/unload/([0-9]+)", LoadUnloadFilamentsHandler),
            (r"/back-filaments-selection", BackLoadUnloadHandler),
            (r"/connectivity", ConnectivityHandler),
            (r"/network-info", ToInfoHandler),
            (r"/ssh-enable", EnableSSHHandler),
            (r"/ssh-disable", DisableSSHHandler),
            (r"/lights", ToLightsHandler),
            (r"/lights/red", LightsHandler),
            (r"/lights/green", LightsHandler),
            (r"/lights/blue", LightsHandler),
            (r"/lights/other", LightsHandler),
            (r"/lights/off", LightsHandler),
            (r"/temperatures", TemperaturesWsHandler),
            (r"/heating-bed", HeatingBedWsHandler),
            (r"/heating-nozzle", HeatingNozzleWsHandler),
            (r"/probe-complete", ProbeCompleteWsHandler),
            (r"/z-probe", ZProbeWsHandler),
            (r"/inspect-grid", InspectGridWsHandler),
            (r"/waiting-file", WaitingFileWsHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "/home/pi/assets"}),
        ]
        tornado.web.Application.__init__(self, handlers, template_path="/home/pi/templates/")
        #Put FirmwareDirector, this is wrong
        self.firmware = SmoothieFirmware()
        self.gpio = Gpio()

class HomeHandler(BasicHandler):
    def get(self):
        if not self.application.gpio.is_initialized:
            self.application.gpio.initialize()
        if not self.firmware.check_mac_address():
            self.render("put_serial.html")        
        elif not self.firmware.check_version():
            self.render("put_version.html", version_list=self.firmware.get_version_list())
        elif not self.firmware.is_initialized:
            self.firmware.initialize()
            self.render("index.html")
        else: self.render("index.html")

class SerialHandler(BasicHandler):
    def post(self):
        serial = self.get_body_argument("serial")
        self.firmware.set_serial(serial)
        #self.firmware.put_config()
        self.render("put_version.html", version_list=self.firmware.get_version_list())

class VersionHandler(BasicHandler):
    def post(self):
        version = self.get_body_argument("version")
        self.firmware.set_version(version)
        self.firmware.initialize()
        self.render("select_calibration.html")

if __name__ == "__main__":
    app = Application()
    parse_command_line()
    app.listen(8888)
    try:
        logging.info('Starting app')
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('Exit success')