from printcore_modified.printcore import printcore
from printcore_modified.plugins.smoothie_event_handler import SmoothieHandler as handler
from gcodes_loader.gcodes_loading import patch_and_split_gcodes
from printcore_modified import gcoder
from firmware.firmware import BaseFirmware
from utils import split_file_for_print, grouper, split_gcode_for_print, get_sd, reset_rpi
import os
import json
import tornado
import os
import itertools
from firmware.the_counter import TheCounter
import logging
import filecmp
import traceback

class SmoothieFirmware(BaseFirmware):

    OFFSET_PATH = "/home/pi/config-files/offsets.json"
    NEW_CONFIG = "/home/pi/v2-firmware/config_files_board/new_hw2/config"
    NEW_CONFIG_OVERRIDE = "/home/pi/v2-firmware/config_files_board/new_hw2/config-override"
    
    def initialize(self):
        """
        Initialized the connection to the board
        and add an event handler
        Check directory for print end
        """
        logger = logging.getLogger('firmware')
        self.board_logger = logging.getLogger('board_logger')
        path = "/home/pi/print_end_status"
        self.printrun = printcore("/dev/ttyACM0", 115200)
        print("Connecting to printer")
        self.the_counter = TheCounter()
        smoothie_handler = handler()
        smoothie_handler.set_the_counter(self.the_counter)
        self.printrun.addEventHandler(smoothie_handler)
        self.is_initialized = True
        #if not os.path.isdir(path):
        #    os.makedirs(path)
        #if not os.listdir(path):
        #    os.system("rm {}/*".format(path))
        #self.printrun.initEventHandlers()

    def homming(self):
        self.printrun.send_now("G28")

    def get_temperatures(self):
        """
        Asyncronous call, so you need a websocket to listen the response
        """
        self.printrun.send_now("M105")

    def reset(self):
        self.printrun.send_now("reset")

    def load_filament(self, extruder):
        self.choose_extruder(extruder)
        self.printrun.send_now("G21")
        self.printrun.send_now("G91")
        self.printrun.send_now("G92 E0")
        self.printrun.send_now("M109 S220")
        self.printrun.send_now("G1 E500 F4000")
        self.printrun.send_now("G1 E78 F80")
        self.printrun.send_now("G92 E0")
        self.printrun.send_now("G4 P35000")
        self.printrun.send_now("M104 S0")

    def unload_filament(self, extruder):
        self.choose_extruder(extruder)
        self.printrun.send_now("G21")
        self.printrun.send_now("G90")
        self.printrun.send_now("M109 S220")
        self.printrun.send_now("G92 E0")
        self.printrun.send_now("G1 E15 F100")
        self.printrun.send_now("G1 E-15 F100")
        #self.printrun.send_now("M109 S180")
        self.printrun.send_now("G4 P20000")
        self.printrun.send_now("G1 E-599 F5000")
        self.printrun.send_now("G92 E0")
        self.printrun.send_now("M104 S0")

    def start_load_filament(self, extruder):
        self.choose_extruder(extruder)
        self.printrun.send_now("G21")
        self.printrun.send_now("M104 S220")

    def start_unload_filament(self, extruder):
        self.choose_extruder(extruder)
        self.printrun.send_now("G21")
        self.printrun.send_now("M104 S215")        

    def extrude_filament(self):
        self.printrun.send_now("G91")
        self.printrun.send_now("G92 E0")
        self.printrun.send_now("G1 E500 F4000")
        self.printrun.send_now("G1 E78 F80")
        self.printrun.send_now("G92 E0")
        #self.printrun.send_now("M104 S0")

    def extrude_one_more(self):
        self.printrun.send_now("G91")
        self.printrun.send_now("G92 E0")
        self.printrun.send_now("G1 E50 F80")
    
    def retract_one_more(self):
        self.printrun.send_now("G91")
        self.printrun.send_now("G92 E0")
        self.printrun.send_now("G1 E-20 F500")
        
    def retract_filament(self):
        self.printrun.send_now("G90")
        self.printrun.send_now("G92 E0")
        self.printrun.send_now("G1 E15 F100")
        self.printrun.send_now("G1 E-15 F100")
        #self.printrun.send_now("M109 S180")
        #self.printrun.send_now("G4 P20000")
        self.printrun.send_now("G1 E-599 F5000")
        self.printrun.send_now("G92 E0")
        #self.printrun.send_now("M104 S0")

    def maintain_temperature(self, temp):
        self.printrun.send_now("M104 S{}".format(temp))

    def cancel(self):
        self.printrun.cancelprint()
        self.printrun.send_now("G28")
        self.printrun.send_now("M104 T0 S0")
        self.printrun.send_now("M104 T1 S0")
        self.printrun.send_now("M140 S0")
        if os.path.exists("/home/pi/cloud/cloud.gcode"):
            os.remove("/home/pi/cloud/cloud.gcode")

    def start_print(self):
        with open(self.OFFSET_PATH) as f:
            config_json = json.load(f)
        with open(self.file_path, errors='ignore') as f:
            gcode = patch_and_split_gcodes(f, config_json["t0_zoffset"])
        self.total_lines = len(gcode)
        self.printrun.startprint(gcode)
        #os.system("cp {} /home/pi/temp/".format(self.file_path))
        #os.system("(head -100 > /home/pi/temp/first/pt1.gcode; cat > /home/pi/temp/first/pt2.gcode) < /home/pi/temp/{}".format(self.filename))
        #os.system("rm /home/pi/temp/{}".format(self.filename))
        #gcode = gcoder.LightGCode([i.strip() for i in open('/home/pi/temp/first/pt1.gcode')])
        #self.printrun.startprint(gcode)
        #os.system("rm /home/pi/temp/first/pt1.gcode")
        #executor = tornado.concurrent.futures.ThreadPoolExecutor(5)
        #tornado.ioloop.IOLoop.current().run_in_executor(executor, split_file_for_print, self.printrun)

    def pause(self):
        self.printrun.pause()
        self.printrun.send_now("G91")
        self.printrun.send_now("G1 Z 5")
        self.printrun.send_now("G91")
        self.printrun.send_now("G0 E-5.5 F1500")
        self.printrun.send_now("G90")
        self.printrun.send_now("G1 X100 Y200 F4000")

    def resume(self):
        self.printrun.send_now("G91")
        self.printrun.send_now("G0 E5.7 F1500")
        self.printrun.send_now("G90")
        self.printrun.resume()

    def direct_pause(self):
        self.printrun.pause()
    
    def direct_resume(self):
        self.printrun.resume()

    def start_print_memory(self):
        with open(self.OFFSET_PATH) as f:
            config_json = json.load(f)
        with open(self.file_path) as f:
            patched_gcode = patch_and_split_gcodes(f, config_json["t0_zoffset"])
        first = list(itertools.islice(patched_gcode, 0, 100))
        gcode = gcoder.LightGCode(first)
        self.printrun.startprint(gcode)
        executor = tornado.concurrent.futures.ThreadPoolExecutor(5)
        tornado.ioloop.IOLoop.current().run_in_executor(executor, split_gcode_for_print, [patched_gcode, self.printrun])
    
    def t0_zoffset_calibration(self, t0_zoffset):
        #with open(self.OFFSET_PATH) as f:
        #    config_json = json.load(f)
        #self.printrun.send_now("G28")
        self.printrun.send_now("T0")
        self.printrun.send_now("G91")
        #self.printrun.send_now("G1 Z5 F7200")
        self.printrun.send_now("G90")
        self.printrun.send_now("G1 X200 F7500")
        self.printrun.send_now("G1 X220 F500")
        self.printrun.send_now("G1 X100 Y100 F7500")
        self.printrun.send_now("G1 Z10 F7500")
        self.printrun.send_now("G30 Z0")
        #self.printrun.send_now("G1 Z{}".format(config_json["t0_zoffset"]))
        self.printrun.send_now("G1 Z{}".format(t0_zoffset))

    def t1_zoffset_calibration(self, t1_zoffset):
        #with open(self.OFFSET_PATH) as f:
        #    config_json = json.load(f)
        #self.printrun.send_now("G28")
        self.printrun.send_now("T0")
        self.printrun.send_now("G1 X100 Y100 F7600")
        self.printrun.send_now("G1 Z10 F7500")
        self.printrun.send_now("G30 Z0")
        self.printrun.send_now("G91")
        self.printrun.send_now("G1 Z5 F7200")
        self.printrun.send_now("G90")
        self.printrun.send_now("G1 X0 F7200")
        self.printrun.send_now("G1 X-12 F500")
        self.printrun.send_now("G1 X128 Y100 F7600")
        self.printrun.send_now("G1 Z{} F7200".format(t1_zoffset))

    def zoffset_up(self):
        self.printrun.send_now("G91")
        self.printrun.send_now("G1 Z0.025")
        self.printrun.send_now("G90")

    def zoffset_down(self):
        self.printrun.send_now("G91")
        self.printrun.send_now("G1 Z-0.025")
        self.printrun.send_now("G90")

    def save_xyoffset(self, x_offset, y_offset):
        with open(self.OFFSET_PATH) as f:
            config_json = json.load(f)
        config_json["t1_xoffset"] = x_offset
        config_json["t1_yoffset"] = y_offset
        config_file = "/home/pi/config-files/confighotend2xyoffset"
        config_smoothie = "/media/smoothie/confighotend2xyoffset"
        info = get_sd()
        sd = info.get(self.hardware_json["board_uuid"])
        if not sd:
            self.board_logger.error('No board uuid found on xy offset')
            return False
        os.system("sudo mount /dev/{} /media/smoothie -o uid=pi,gid=pi".format(sd))
        with open(config_file, "w") as f:
            f.write("extruder.hotend2.y_offset {}\n".format(str(y_offset)))
            f.write("extruder.hotend2.x_offset {}".format(str(x_offset)))
        os.system("cp {} /media/smoothie/confighotend2xyoffset && sync".format(config_file))
        os.system("sudo umount /media/smoothie")
        check_res = self.check_config(config_file, config_smoothie)
        if check_res:
            with open(self.OFFSET_PATH, 'w') as f:
                json.dump(config_json, f)
            self.config_retry = 0
            return check_res
        elif self.config_retry < self.config_max_retries:
            self.board_logger.error('Error saving xy offset, attemp {}'.format(str(self.config_retry)))
            self.config_retry = self.config_retry + 1
            self.save_xyoffset(x_offset, y_offset)
        else:
            self.board_logger.error('Error saving xy offset after all attemps')
            self.config_retry = 0
            return check_res


    def save_zoffset(self, z_offset_t0=None, z_offset_t1=None):
        with open(self.OFFSET_PATH) as f:
            config_json = json.load(f)
        if not z_offset_t0 and not z_offset_t1:
            z_offset_t0 = config_json["t0_zoffset"]
            z_offset_t1 = config_json["t1_zoffset"]
        elif not z_offset_t0 and z_offset_t1:
            z_offset_t0 = config_json["t0_zoffset"]
            config_json["t1_zoffset"] = z_offset_t1
        elif not z_offset_t1 and z_offset_t0:
            z_offset_t1 = config_json["t1_zoffset"]
            config_json["t0_zoffset"] = z_offset_t0
        else:
            config_json["t0_zoffset"] = z_offset_t0
            config_json["t1_zoffset"] = z_offset_t1
        config_file = "/home/pi/config-files/confighotendzoffset"
        config_smoothie = "/media/smoothie/confighotendzoffset"
        with open(self.OFFSET_PATH, 'w') as f:
            json.dump(config_json, f)
        info = get_sd()
        sd = info.get(self.hardware_json["board_uuid"])
        if not sd:
            self.board_logger.error('Not board uuid found on z offset')
            return False
        os.system("sudo mount /dev/{} /media/smoothie -o uid=pi,gid=pi".format(sd))
        with open(config_file, "w") as f:
            f.write("extruder.hotend2.z_offset {}".format(str(round(float(z_offset_t1) - float(z_offset_t0), 2))))
        os.system("cp {} /media/smoothie/confighotendzoffset && sync".format(config_file))
        os.system("sudo umount /media/smoothie")
        check_res = self.check_config(config_file, config_smoothie)
        if check_res:
            return check_res
        elif self.config_retry < self.config_max_retries:
            self.config_retry = self.config_retry + 1
            self.save_zoffset(z_offset_t0, z_offset_t1)
        else:
            self.board_logger.error('Error saving z offset after all attemps')
            self.config_retry = 0
            return check_res

    def give_calibration_page(self):
        return "25_calibration.html"

    def calibration_25_points_until_complete(self):
        #self.printrun.send_now("G28")
        self.printrun.send_now("G32")
        #self.printrun.send_now("M374")
        #self.printrun.send_now("M500")

    def calibration_25_points_for_complete(self):
        self.printrun.send_now("M374")
        self.printrun.send_now("M500")
        self.printrun.send_now("G28")

    def show_grid_25_points(self):
        self.printrun.send_now("M375.1")

    def reset_grid(self):
        self.printrun.send_now("M561")
        self.printrun.send_now("M500")
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

    def put_config(self):
        info = get_sd()
        sd = info.get(self.hardware_json["board_uuid"])
        if not sd:
            self.board_logger.error('Board uuid not found in config')
            return 1
        os.system("sudo mount /dev/{} /media/smoothie -o uid=pi,gid=pi".format(sd))
        os.system("cp {} /media/smoothie/ && sync".format(self.NEW_CONFIG))
        os.system("cp {} /media/smoothie/ && sync".format(self.NEW_CONFIG_OVERRIDE))
        os.system("sudo umount /media/smoothie")
        check_res = self.check_config("/media/smoothie/config", self.NEW_CONFIG,
                        second_conf_rpi="/media/smoothie/config-override",
                        second_conf=self.NEW_CONFIG_OVERRIDE)
        if check_res:
            os.system("touch /home/pi/config_updated")
            self.reset()
            reset_rpi()
            return 0
        elif self.config_retry < self.config_max_retries:
            self.board_logger.error('Error saving config on smoothie, attemp {}'.format(str(self.config_retry)))
            self.config_retry = self.config_retry + 1
            self.put_config()
        else:
            return 2


    def choose_extruder(self, extruder):
        if extruder == "ext_1":
            self.move_to_t0()
        elif extruder == "ext_2":
            self.move_to_t1()

    def move_to_t0(self):
        self.printrun.send_now("G28 XY")
        self.printrun.send_now("T0")
        self.printrun.send_now("G91")
        self.printrun.send_now("G90")
        self.printrun.send_now("G1 X200 F7500")
        self.printrun.send_now("G1 X220 F500")
        self.printrun.send_now("G1 X128 Y100 F7500")
        self.printrun.send_now("G1 F7500")
        self.printrun.send_now("T0")

    def move_to_t1(self):
        self.printrun.send_now("G28 XY")
        self.printrun.send_now("T0")
        self.printrun.send_now("G91")
        self.printrun.send_now("G90")
        self.printrun.send_now("G1 X100 Y100 F7500")
        self.printrun.send_now("G1 X0 F7200")
        self.printrun.send_now("G1 X-12 F500")
        self.printrun.send_now("G1 X100 Y100 F7500")
        self.printrun.send_now("G1 F7500")
        self.printrun.send_now("T1")

    def bed_up(self):
        self.printrun.send_now("G91")
        self.printrun.send_now("G1 Z-35")
        self.printrun.send_now("G90")

    def bed_down(self):
        self.printrun.send_now("G91")
        self.printrun.send_now("G1 Z 35")
        self.printrun.send_now("G90")

    def bed_home(self):
        self.printrun.send_now("G28 Z")
    
    def bed_temperature(self, temp):
        self.printrun.send_now("M140 S{}".format(temp))

    def heat_extruder(self, temp, extruder):
        self.printrun.send_now("M104 S{} {}".format(temp, extruder))

    def cold_extruders(self):
        self.printrun.send_now("M104 S0 T0")
        self.printrun.send_now("M104 S0 T1")

    def extrude(self, extruder):
        self.printrun.send_now(extruder)
        self.printrun.send_now("G90")
        self.printrun.send_now("G92 E0")
        self.printrun.send_now("G1 E20 F80")
        self.printrun.send_now("G92 E0")

    def retract(self, extruder):
        self.printrun.send_now(extruder)
        self.printrun.send_now("G90")
        self.printrun.send_now("G92 E0")
        self.printrun.send_now("G1 E-20 F500")
        self.printrun.send_now("G92 E0")

    def turn_off_motors(self):
        self.printrun.send_now("M18")

    def turn_on_motors(self):
        self.printrun.send_now("M17")

    def set_nozzle_size(self, nozzle, size):
        if nozzle == "1":
            self.user_conf_json["nozzle_1"] = size
        elif nozzle == "2":
            self.user_conf_json["nozzle_2"] = size

    def check_config(self, config_rpi, config_smoothie, second_conf_rpi = None, second_conf = None):
        info = get_sd()
        sd = info.get(self.hardware_json["board_uuid"])
        resp_cmp = False
        os.system("sudo mount /dev/{} /media/smoothie -o uid=pi,gid=pi".format(sd))
        try:
            if second_conf:
                resp_1 = filecmp.cmp(config_smoothie, config_rpi)
                resp_2 = filecmp.cmp(second_conf, second_conf_rpi)
                resp_cmp = resp_1 and resp_2
            else:
                resp_cmp = filecmp.cmp(config_smoothie, config_rpi)
            os.system("sudo umount /media/smoothie")
        except Exception:
            self.board_logger.error(str(traceback.format_exc()))
        finally:
            return resp_cmp