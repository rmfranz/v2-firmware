from firmware.smoothie_firmware import SmoothieFirmware

class SmoothieFirmware3PT(SmoothieFirmware):

    NEW_CONFIG = "/home/pi/v2-firmware/config_files_board/new_hw1/config"
    
    def make_calibration(self):
        self.printrun.send_now("G90")
        self.printrun.send_now("G28")
        self.printrun.send_now("G1 Z5 F4000")
        self.printrun.send_now("G32")
        self.printrun.send_now("M500")
        #self.printrun.send_now("G28")

    def give_calibration_page(self):
        return "3_calibration.html"