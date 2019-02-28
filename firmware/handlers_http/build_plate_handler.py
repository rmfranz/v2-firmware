from handlers_http.basic_handler import BasicHandler
import collections

class ToBuildPlateControlHandler(BasicHandler):
    def get(self):
        self.firmware.homming()
        self.render("plate_control.html")

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

class ToPlateTemperatureHandler(BasicHandler):
    def get(self):
        mat_temps = {
            "ABS ~ 95°C": 95,
            "Flex (PU) ~ 70°C": 70,
            "HIPS ~ 95°C": 95,
            "Nylon ~ 85°C": 85,
            "PETG ~ 70°C": 70,
            "PLA Tough ~ 60°C": 60,
            "PLA+ ~ 60°C": 60,
            "PVA ~ 50°C": 50,
            "OFF ~ 0°C": 0,
        }
        mat_temps = collections.OrderedDict(sorted(mat_temps.items()))
        mat_temps.move_to_end('OFF ~ 0°C')
        self.render("bed_temperatures.html", mat_temps=mat_temps)

class PlateTemperatureHandler(BasicHandler):
    def get(self, temp):
        self.firmware.bed_temperature(temp)
        self.redirect("/build-plate-controls")