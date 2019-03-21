import json

class Wizzard():

    WIZZARD_JSON_FOLDER = "/home/pi/config-files/wizzard.json"

    def __init__(self):
        with open(self.WIZZARD_JSON_FOLDER) as f:
            self.wizzard_json = json.load(f)
        self.viewed = False
        self.warning_viewed = False
        self.wifi_viewed = False
        self.update_viewed = False
        self.cloud_viewed = False
        self.filament_viewed = False

    def give_me_page(self):
        if self.wizzard_json["update_warning"] and not self.warning_viewed:
            self.warning_viewed = True
            return "/update-warning"
        if not self.wizzard_json["lang"]:
            self.wizzard_json["lang"] = True
            self.write_wizzard()
            return "/language"
        if self.wizzard_json["wifi"] == "not_selected" and not self.wifi_viewed:
            self.wifi_viewed = True
            #TODO: Check connectivity, si hay internet seguir con el siguiente
            return "/wifi-connection"
        if self.wizzard_json["update"] == "not_selected" and not self.update_viewed:
            self.update_viewed = True
            #TODO: Check update, si no hay un update seguir
            return "/software-update"
        if self.wizzard_json["cloud"] == "not_selected" and not self.cloud_viewed:
            self.cloud_viewed = True
            return "/to-cloud"
        if self.wizzard_json["filament"] == "not_selected" and not self.filament_viewed:
            self.filament_viewed = True
            return "/filaments-selection"
        self.viewed = True
        return "/home"

    def write_wizzard(self):
        with open(self.WIZZARD_JSON_FOLDER, 'w') as f:
            json.dump(self.wizzard_json, f)
