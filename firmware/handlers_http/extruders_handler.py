from handlers_http.basic_handler import BasicHandler

class ToExtrudersControlHandler(BasicHandler):
    def get(self):
        self.firmware.homming()
        self.render("extruders_control.html")

class PlateUpHandler(BasicHandler):
    def get(self):
        self.firmware.bed_up()
        self.write("ok")

class PlateDownHandler(BasicHandler):
    def get(self):
        self.firmware.bed_down()
        self.write("ok")

class PlateHomeHandler(BasicHandler):
    def get(self):
        self.firmware.bed_home()
        self.write("ok")

class ToExtruderTemperatureHandler(BasicHandler):
    def get(self):
        self.render("extruder_temp.html")

class PlateTemperatureHandler(BasicHandler):
    def get(self, temp):
        self.firmware.bed_temperature(temp)
        self.redirect("/build-plate-controls")