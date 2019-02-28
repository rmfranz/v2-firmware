from handlers_http.basic_handler import BasicHandler
from utils import get_extruder
import collections

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
        extruder = self.request.path.split("/")[1]
        self.firmware.choose_extruder(extruder)
        mat_temps = {
            "ABS ~ 240°C": 240,
            "Flex (PU) ~ 235°C": 235,
            "HIPS ~ 240°C": 240,
            "Nylon ~ 240°C": 240,
            "PETG ~ 240°C": 240,
            "PLA Tough ~ 215°C": 215,
            "PLA+ ~ 205°C": 205,
            "PVA ~ 195°C": 195,
            "OFF ~ 0°C": 0,
        }
        mat_temps = collections.OrderedDict(sorted(mat_temps.items()))
        mat_temps.move_to_end('OFF ~ 0°C')
        self.render("extruder_temp.html", extruder=extruder, mat_temps=mat_temps)

class ExtruderTemperatureHandler(BasicHandler):
    def get(self, temp):
        extruder = get_extruder(self.request.path.split("/")[1])
        self.firmware.heat_extruder(temp, extruder)
        if temp == 0:
            self.clear_cookie("extruder")
            self.clear_cookie("extruder_temp")
        else:
            self.set_cookie("extruder", extruder)
            self.set_cookie("extruder_temp", temp)
        self.redirect("/extruders-controls")

class GetExtrudersControlHandler(BasicHandler):
    def get(self):
        extruder = self.get_cookie("extruder", default="T0")
        extruder_temp = self.get_cookie("extruder_temp", default=0)
        self.write({"extruder" : extruder, "extruder_temp": extruder_temp})

class PlateTemperatureHandler(BasicHandler):
    def get(self, temp):
        self.firmware.bed_temperature(temp)
        self.redirect("/build-plate-controls")

class ExtruderActionHandler(BasicHandler):
    def get(self):
        extruder = get_extruder(self.request.path.split("/")[1])
        action = self.request.path.split("/")[2]
        if action == "extrude":
            self.firmware.extrude(extruder)
        elif action == "retract":
            self.firmware.retract(extruder)
        self.write("ok")