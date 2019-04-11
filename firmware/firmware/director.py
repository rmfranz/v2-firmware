from firmware.smoothie_firmware import SmoothieFirmware
from firmware.smoothie_firmware_3pt import SmoothieFirmware3PT
from firmware.firmware import BaseFirmware

import json

class FirmwareDirector:
    def __init__(self):
        with open("/home/pi/config-files/hardware.json") as f:
            self.hardware_json = json.load(f)
    
    def give_me_firmware(self):
        if self.hardware_json["hw_version"] == "HV1":
            return SmoothieFirmware3PT()
        elif self.hardware_json["hw_version"] == "HV2":
            return SmoothieFirmware()
        else:
            # Need a default one
            return BaseFirmware()