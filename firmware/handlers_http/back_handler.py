from handlers_http.basic_handler import BasicHandler
import os

class BackSelectCalibrationHandler(BasicHandler):
    def get(self):
        self.firmware.homming()
        self.render("select_calibration.html")

class BackLoadUnloadHandler(BasicHandler):
    def get(self):
        #self.firmware.homming()
        self.redirect("/filaments-selection")

class BackPlateHandler(BasicHandler):
    def get(self):
        #self.firmware.bed_temperature(0)
        #self.firmware.homming()
        lights_on = "true"
        if not self.application.gpio.lights_on:
            lights_on = "false"
        self.render("manual_ctl_select.html", lights_on=lights_on)

class BackExtruderHandler(BasicHandler):
    def get(self):
        #self.firmware.heat_extruder(0, "T0")
        #self.firmware.heat_extruder(0, "T1")
        #self.firmware.homming()
        #self.clear_cookie("extruder")
        #self.clear_cookie("extruder_temp")
        lights_on = "true"
        if not self.application.gpio.lights_on:
            lights_on = "false"
        self.render("manual_ctl_select.html", lights_on=lights_on)

class BackLoadUnloadActionHandler(BasicHandler):
    def get(self):
        self.firmware.cold_extruders()
        #self.firmware.homming()
        self.redirect("/filaments-selection")

class BackPrintFinishedHandler(BasicHandler):
    def get(self):
        self.firmware.homming()
        self.application.gpio.lights_blue()
        if os.path.exists("/home/pi/print_images/print.png"):
            os.remove("/home/pi/print_images/print.png")
        self.redirect("/home")