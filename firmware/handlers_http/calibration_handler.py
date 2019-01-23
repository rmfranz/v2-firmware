from handlers_http.basic_handler import BasicHandler
import tornado
import json

class BuildPlateCalibrationHandler(BasicHandler):
    
    def get(self):
        #Aca hay que poner la qué calibración va
        self.render("25_calibration.html")

class Points25Calibration(BasicHandler):
    def get(self):
        self.firmware.calibration_25_points_until_complete()
        self.write("ok")

class Show25GridCalibration(BasicHandler):
    def get(self):
        self.firmware.show_grid_25_points()
        self.write("ok")

class SavePoints25Calibration(BasicHandler):
    def get(self):
        self.firmware.calibration_25_points_for_complete()
        self.render("select_calibration.html")

class Points3Calibration(BasicHandler):
    def get(self):
        self.firmware.move_to_p1(1)
        self.render("3_calibration.html")

class ZOffsetCalibrationHandler(BasicHandler):
    
    def get(self):
        self.firmware.t0_zoffset_calibration()
        self.render("z_offset_calibration.html")

    def post(self):
        zoffset_t0 = self.get_body_argument("zoffset_t0")
        zoffset_t1 = self.get_body_argument("zoffset_t1")
        response = self.firmware.save_zoffset(zoffset_t0, zoffset_t1)
        # si la respuesta es 0, todo bien sino todo mal
        if response == 0:
            self.firmware.reset()
            self.firmware.disconnect()
            tornado.ioloop.IOLoop.current().call_later(delay=20,
                callback=self.firmware.reconnect)
            self.write("ok")
        else:
            self.render("error")

class ZOffsetT0CalibrationHandler(BasicHandler):
    
    def get(self):
        self.firmware.t0_zoffset_calibration()
        self.write("ok")

class ZOffsetT1CalibrationHandler(BasicHandler):
    
    def get(self):
        self.firmware.t1_zoffset_calibration()
        self.write("ok")

class GetOffsetsHandler(BasicHandler):

    def get(self):
        with open(self.OFFSET_PATH) as f:
            config_json = json.load(f)
        self.write(config_json)

class UpZOffsetCalibrationHandler(BasicHandler):
    
    def get(self):
        self.firmware.zoffset_up()
        self.write("ok")

class DownZOffsetCalibrationHandler(BasicHandler):
    
    def get(self):
        self.firmware.zoffset_down()
        self.write("ok")