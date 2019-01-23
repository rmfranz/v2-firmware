import tornado.web
import tornado.websocket
from printcore_modified.printcore import printcore
from tornado.options import parse_command_line
from tornado.options import define, options
from handlers_http.print_handler import * 
from handlers_http.basic_handler import * 
from handlers_http.calibration_handler import *
from handlers_http.back_handler import *
from handlers_websocket.temperatures_ws_handler import *
from handlers_websocket.calibration_ws_handler import *
from handlers_http.setup_handler import *
from firmware.smoothie_firmware import SmoothieFirmware
import logging
import pickle
import os

define("template_folder", default="templates/", help="Folder to use")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/home", HomeHandler),
            (r"/print", PrintHandler),
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
            (r"/back-calibration-selection", BackSelectCalibrationHandler),
            (r"/get-offsets", GetOffsetsHandler),
            (r"/t0-calibration", ZOffsetT0CalibrationHandler),
            (r"/t1-calibration", ZOffsetT1CalibrationHandler),
            (r"/z-offset-up", UpZOffsetCalibrationHandler),
            (r"/z-offset-down", DownZOffsetCalibrationHandler),
            (r"/build-plate-calibration", BuildPlateCalibrationHandler),
            (r"/z-offset-calibration", ZOffsetCalibrationHandler),
            (r"/points-25-calibration", Points25Calibration),
            (r"/save-25-calibration", SavePoints25Calibration),
            (r"/setup", SetupHandler),
            (r"/temperatures", TemperaturesWsHandler),
            (r"/heating-bed", HeatingBedWsHandler),
            (r"/heating-nozzle", HeatingNozzleWsHandler),
            (r"/probe-complete", ProbeCompleteWsHandler),
            (r"/z-probe", ZProbeWsHandler),
            (r"/inspect-grid", InspectGridWsHandler),
            (r"/show-grid", Show25GridCalibration),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "/home/pi/prueba/assets"}),
        ]
        tornado.web.Application.__init__(self, handlers,
                                         autoreload=True, template_path="/home/pi/prueba/templates/")
        #Put FirmwareDirector, this is wrong
        self.firmware = SmoothieFirmware()

class HomeHandler(BasicHandler):
    def get(self):
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