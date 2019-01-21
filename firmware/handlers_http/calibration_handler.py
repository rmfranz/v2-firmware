from handlers_http.basic_handler import BasicHandler

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