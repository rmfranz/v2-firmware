import json
from getmac import get_mac_address


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
        self.is_initialiced = False
    
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
        self.hardware_json["serial_number"] = serial
        self.write_hardware_json()

    def get_version_list(self):
        return list(self.version_json)
    
    def write_hardware_json(self):
        with open(self.HARDWARE_JSON_FOLDER, 'w') as f:
                json.dump(self.hardware_json, f)



class SmoothieFirmware(BaseFirmware):
    pass