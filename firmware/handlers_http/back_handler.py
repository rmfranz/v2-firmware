from handlers_http.basic_handler import BasicHandler

class BackSelectCalibrationHandler(BasicHandler):
    def get(self):
        self.firmware.homming()
        self.render("select_calibration.html")

class BackLoadUnloadHandler(BasicHandler):
    def get(self):
        self.firmware.homming()
        self.render("filaments_selection.html")

class BackPlateHandler(BasicHandler):
    def get(self):
        self.firmware.bed_temperature(0)
        self.firmware.homming()
        self.render("manual_ctl_select.html")