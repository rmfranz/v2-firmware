from handlers_http.basic_handler import BasicHandler
from tornado.options import options

class BuildPlateCalibrationHandler(BasicHandler):
    
    def get(self):
        self.render(options.template_folder + "25_calibration.html")

class ZOffsetCalibrationHandler(BasicHandler):
    
    def get(self):
        self.render(options.template_folder + "z_offset_calibration.html")