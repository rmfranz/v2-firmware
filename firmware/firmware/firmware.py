import json
from getmac import get_mac_address
import glob
import tornado
from subprocess import check_output

class FirmwareDirector:
    pass

class BaseFirmware:

    HARDWARE_JSON_FOLDER = "firmware/firmware_jsons/hardware.json"

    def __init__(self):
        with open("firmware/firmware_jsons/version.json") as f:
            self.version_json = json.load(f)
        with open(self.HARDWARE_JSON_FOLDER) as f:
            self.hardware_json = json.load(f)
        with open("firmware/firmware_jsons/filaments.json") as f:
            self.filaments_json = json.load(f)
        self.mac_addres_checked = False
        self.is_initialized = False
        self.printrun = None

    def init_ws_handler(self):
        self.printrun.initEventHandlers()
    
    def check_mac_address(self):
        """
            First check if in life cycle of the application the mac address was checked
            If not, proceed to check mac address on file and save
        """
        if self.mac_addres_checked:
            return self.mac_addres_checked
        check = self.hardware_json["mac_address_eth0"] == get_mac_address(interface="eth0")
        self.mac_addres_checked = True
        if not check:
            self.hardware_json["mac_address_eth0"] = get_mac_address(interface="eth0")
            self.write_hardware_json()
        return check

    def check_version(self):
        return self.hardware_json["hw_version"]
    
    def set_version(self, version):
        self.hardware_json["hw_version"] = version
        self.write_hardware_json()
    
    def set_serial(self, serial):
        #TODO: Check if more than one
        board_info = check_output("ls -l /dev/disk/by-uuid | grep sd", shell=True, universal_newlines=True)
        board_info = [j for j in board_info.split("\n") if j]
        self.hardware_json["board_uuid"] = board_info[0].split()[8]
        self.hardware_json["serial_number"] = serial
        self.write_hardware_json()

    def get_version_list(self):
        #return list(self.version_json)
        return ["KPA1"]
    
    def write_hardware_json(self):
        with open(self.HARDWARE_JSON_FOLDER, 'w') as f:
                json.dump(self.hardware_json, f)
    
    def reconnect(self):
        """
        list directory /dev/ttyACM* because smoothie board should be on
        /dev/ttyACM0 or /dev/ttyACM1 and there should not be anything else there
        """
        dev_list = glob.glob('/dev/ttyACM*')
        if dev_list:
            self.printrun.connect(port=dev_list[0])
        else:
            tornado.ioloop.IOLoop.current().call_later(delay=20,
                callback=self.reconnect)

    def disconnect(self):
        self.printrun.disconnect()

    def pause(self):
        self.printrun.pause()

    def resume(self):
        self.printrun.resume()