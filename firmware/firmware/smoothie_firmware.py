from printcore_modified.printcore import printcore
from printcore_modified.plugins.smoothie_event_handler import SmoothieHandler as handler
from firmware.firmware import BaseFirmware
from gcodes_loader.gcodes_loading import patch_and_split_gcodes
from printcore_modified import gcoder
import os

class SmoothieFirmware(BaseFirmware):
    
    def initialize(self):
        """
        Initialized the connection to the board
        and add an event handler
        """
        self.printrun = printcore("/dev/ttyACM0", 115200)
        print("Conecte la impresora")
        self.printrun.addEventHandler(handler())
        #self.printrun.initEventHandlers()
        self.is_initialized = True

    def homming(self):
        self.printrun.send_now("G28")

    def get_temperatures(self):
        """
        Asyncronous call, so you need a websocket to listen the response
        """
        self.printrun.send_now("M105")

    def reset(self):
        self.printrun.send_now("reset")

    def cancel(self):
        self.printrun.cancelprint()
        self.printrun.send_now("G28")
        self.printrun.send_now("M104 S0")
        self.printrun.send_now("M140 S0")

    def start_print(self, gcode_path):
        with open(gcode_path) as f:
            gcode = gcoder.LightGCode(patch_and_split_gcodes(f))
            self.printrun.startprint(gcode)
    
    def t0_zoffset_calibration(self):
        self.printrun.send_now("G28")
        self.printrun.send_now("T0")
        self.printrun.send_now("G91")
        self.printrun.send_now("G1 Z3 F7200")
        self.printrun.send_now("G90")
        self.printrun.send_now("G1 X200 F7500")
        self.printrun.send_now("G1 X220 F500")
        self.printrun.send_now("G1 X100 Y100 F7500")
        self.printrun.send_now("G1 Z10 F7500")
        self.printrun.send_now("G30 Z0")
        #self.printrun.send_now("G1 Z1")

    def t1_zoffset_calibration(self):
        self.printrun.send_now("G28")
        self.printrun.send_now("T0")
        self.printrun.send_now("G1 X100 Y100 F7600")
        self.printrun.send_now("G1 Z10 F7500")
        self.printrun.send_now("G30 Z0")
        self.printrun.send_now("G91")
        self.printrun.send_now("G1 Z3 F7200")
        self.printrun.send_now("G90")
        self.printrun.send_now("G1 X0 F7200")
        self.printrun.send_now("G1 X-12 F500")
        self.printrun.send_now("G1 X128 Y100 F7600")
        self.printrun.send_now("G1 Z3 F7200")

    def zoffset_up(self):
        self.printrun.send_now("G91")
        self.printrun.send_now("G1 Z0.025")
        self.printrun.send_now("G90")

    def zoffset_down(self):
        self.printrun.send_now("G91")
        self.printrun.send_now("G1 Z-0.025")
        self.printrun.send_now("G90")

    def save_zoffset_t0(self, z_offset):
        config_file = "/home/pi/config-files/confighotend1offset"
        os.system("sudo mount /dev/sda1 /media/smoothie -o uid=pi,gid=pi")
        with open(config_file, "w") as f:
            f.write("extruder.hotend1.z_offset {}".format(str(z_offset)))
        os.system("cp {} /media/smoothie/confighotend1offset && sync".format(config_file))
        response = os.system("sudo umount /media/smoothie")
        return response

    def calibration_25_points_until_complete(self):
        self.printrun.send_now("G28")
        self.printrun.send_now("G32")

    def calibration_25_points_for_complete(self):
        self.printrun.send_now("M374")
        self.printrun.send_now("G28")

    def move_to_p1(self, z_probe):
        self.printrun.send_now("G28")
        self.printrun.send_now("G1 Z10 F9000")
        self.printrun.send_now("G1 X100 Y200")
        self.printrun.send_now("G30 Z0")
        self.printrun.send_now("G1 Z{}".format(z_probe))

    def move_to_p2(self, z_probe):
        self.printrun.send_now("G28")
        self.printrun.send_now("G1 Z10 F9000")
        self.printrun.send_now("G1 X0 Y10")
        self.printrun.send_now("G30 Z0")
        self.printrun.send_now("G1 Z{}".format(z_probe))

    def move_to_p3(self, z_probe):
        self.printrun.send_now("G28")
        self.printrun.send_now("G1 Z10 F9000")
        self.printrun.send_now("G1 X180 Y10")
        self.printrun.send_now("G30 Z0")
        self.printrun.send_now("G1 Z{}".format(z_probe))