from firmware.smoothie_firmware import SmoothieFirmware

class SmoothieFirmware3PT(SmoothieFirmware):
    
    def make_calibration(self):
        self.printrun.send_now("G90")
        self.printrun.send_now("G28")
        self.printrun.send_now("G1 Z5 F4000")
        self.printrun.send_now("G32")
        self.printrun.send_now("M500")
        #self.printrun.send_now("G28")

    def give_calibration_page(self):
        return "3_calibration.html"