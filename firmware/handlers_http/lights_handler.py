from handlers_http.basic_handler import BasicHandler

class LightsHandler(BasicHandler):
    def get(self):
        color = self.request.path.split("/")[2]
        if "red" in color:
            self.application.gpio.lights_red()
        elif "green" in color:
            self.application.gpio.lights_green()
        elif "blue" in color:
            self.application.gpio.lights_blue()
        elif "other" in color:
            self.application.gpio.lights_other()
        elif "light_blue" in color:
            self.application.gpio.lights_light_blue()
        elif "orange" in color:
            self.application.gpio.lights_orange()
        elif "white" in color:
            self.application.gpio.lights_white()
        elif "off" in color:
            self.application.gpio.lights_off()
        self.write("ok")

class ToLightsHandler(BasicHandler):
    def get(self):
        self.render("lights_colors.html")