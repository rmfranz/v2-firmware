from handlers_http.basic_handler import BasicHandler

class BackSelectCalibrationHandler(BasicHandler):
    def get(self):
        self.firmware.homming()
        self.render("select_calibration.html")

class BackLoadUnloadHandler(BasicHandler):
    def get(self):
        self.firmware.homming()
        self.render("filaments_selection.html")