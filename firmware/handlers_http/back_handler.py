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

class BackExtruderHandler(BasicHandler):
    def get(self):
        self.firmware.heat_extruder(0, "T0")
        self.firmware.heat_extruder(0, "T1")
        self.firmware.homming()
        self.clear_cookie("extruder")
        self.clear_cookie("extruder_temp")
        self.render("manual_ctl_select.html")