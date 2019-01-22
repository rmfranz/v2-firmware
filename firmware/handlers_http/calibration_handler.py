from handlers_http.basic_handler import BasicHandler
import tornado

class BuildPlateCalibrationHandler(BasicHandler):
    
    def get(self):
        #Aca hay que poner la qué calibración va
        self.render("25_calibration.html")

class Points25Calibration(BasicHandler):
    def get(self):
        self.firmware.calibration_25_points_until_complete()
        self.render("25_calibration.html")

class Points3Calibration(BasicHandler):
    def get(self):
        self.firmware.move_to_p1(1)
        self.render("3_calibration.html")

class ZOffsetCalibrationHandler(BasicHandler):
    
    def get(self):
        self.firmware.t0_zoffset_calibration()
        self.render("z_offset_calibration.html")

    def post(self):
        z_offset = self.get_body_argument("zoffset")
        response = self.firmware.save_zoffset_t0(z_offset)
        # si la respuesta es 0, todo bien sino todo mal
        if response == 0:
            self.firmware.reset()
            self.firmware.disconnect()
            tornado.ioloop.IOLoop.current().call_later(delay=20,
                callback=self.firmware.reconnect)
            self.render("select_calibration.html")
        else:
            self.render("z_offset_calibration.html")
            

class UpZOffsetCalibrationHandler(BasicHandler):
    
    def get(self):
        self.firmware.zoffset_up()
        self.write("ok")

class DownZOffsetCalibrationHandler(BasicHandler):
    
    def get(self):
        self.firmware.zoffset_down()
        self.write("ok")