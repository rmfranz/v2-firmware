import os, fnmatch
from subprocess import check_output, call
from printcore_modified import gcoder
import itertools
from websocket import create_connection
import time
import re
import tornado

def perform_os_check():
    if not os.path.exists("/home/pi/config-files"):
        os.mkdir("/home/pi/config-files")
        os.system("cp /home/pi/v2-firmware/config_files_board/offsets.json /home/pi/config-files/offsets.json")
        os.system("cp /home/pi/v2-firmware/config_files_board/hardware.json /home/pi/config-files/hardware.json")
        os.system("cp /home/pi/v2-firmware/config_files_board/user_conf.json /home/pi/config-files/user_conf.json")
        os.system("cp /home/pi/v2-firmware/config_files_board/confighotend2xyoffset /home/pi/config-files/confighotend2xyoffset")
        os.system("cp /home/pi/v2-firmware/config_files_board/confighotendzoffset /home/pi/config-files/confighotendzoffset")
        os.system("cp /home/pi/v2-firmware/config_files_board/config /home/pi/config-files/config")
        os.system("cp /home/pi/v2-firmware/config_files_board/on_boot.gcode /home/pi/config-files/on_boot.gcode")

def mount_usb(uuid_board):
    if not check_output("ls /media/usb", shell=True, universal_newlines=True):
        #TODO: Check if more than one
        usb_info = check_output("ls -l /dev/disk/by-uuid | grep sd | grep -v {}".format(uuid_board),
                        shell=True, universal_newlines=True)
        #a = check_output("ls -l /dev/disk/by-uuid | grep sd", shell=True, universal_newlines=True)
        usb_info = [j for j in usb_info.split("\n") if j]
        #usb = {usb_info[0].split()[8]: usb_info[0].split()[10].split("/")[-1]}
        return os.system("sudo mount /dev/{} /media/usb -o uid=pi,gid=pi".format(usb_info[0].split()[10].split("/")[-1]))
    else: return 0

def get_gcodes_from_usb():
    dirName = "/media/usb"
    pattern = "*.gcode"
    dict_of_files = {}
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        dict_of_files.update({file: os.path.join(dirpath, file) for file in filenames if fnmatch.fnmatch(file, pattern)})
    return dict_of_files

def get_gcodes_from_sample():
    dirName = "/home/pi/v2-firmware/Samples"
    pattern = "*.gcode"
    dict_of_files = {}
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        dict_of_files.update({file: os.path.join(dirpath, file) for file in filenames if fnmatch.fnmatch(file, pattern)})
    return dict_of_files

def get_gcodes_from_calibration():
    dirName = "/home/pi/v2-firmware/calibrationObjects"
    pattern = "*.gcode"
    dict_of_files = {}
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        dict_of_files.update({file: os.path.join(dirpath, file) for file in filenames if fnmatch.fnmatch(file, pattern)})
    return dict_of_files

def scan_wlan():
    """
    There is an alternative with iw, but gives other result string
       check_output("sudo iw wlan0 scan | grep SSID | tr -s ' '", shell=True, universal_newlines=True)
    """
    scanoutput = check_output("sudo iwlist wlan0 scan | grep ESSID | tr -s ' '", shell=True, universal_newlines=True)
    list_ssid = filter(None, [raw_ssid.split('"')[0] for raw_ssid in scanoutput.split('ESSID:"') if raw_ssid.strip()])
    return list(list_ssid)

def connect_public_wifi(network_name):
    network_number = int(check_output("wpa_cli add_network | grep -v \"Selected interface 'p2p-dev-wlan0'\"", shell=True, universal_newlines=True))
    os.system("sudo mount -o remount,rw /")
    os.system("sudo wpa_cli set_network {} ssid '\"{}\"'".format(network_number, network_name))
    os.system("sudo wpa_cli set_network {} key_mgmt NONE".format(network_number))
    os.system("sudo wpa_cli enable_network {}".format(network_number))
    os.system("sudo wpa_cli select_network {}".format(network_number))
    os.system("sudo wpa_cli save_config")
    os.system("sudo wpa_cli -i wlan0 reconfigure")
    os.system("sudo mount -o remount,ro /")
    time.sleep(5)
    return wifi_connected()

@tornado.gen.coroutine
def connect_private_wifi(network_name, password):
    wpa_conf_path = "/home/pi/wpa_supplicant.conf"
    wpa_conf_raw = "/home/pi/v2-firmware/config_files_board/wpa_supplicant.conf"
    with open(wpa_conf_raw, 'r') as f:
        conf = f.read()
    conf = conf.replace("ssid_replace", network_name)
    conf = conf.replace("psk_replace", password)
    with open(wpa_conf_path, 'w') as f:
        f.write(conf)
    os.system("sudo pkill -TERM wpa_supplicant")
    yield tornado.gen.sleep(1)
    os.system("sudo wpa_supplicant -B -c/etc/wpa_supplicant/wpa_supplicant.conf -iwlan0 -Dnl80211,wext")
    yield tornado.gen.sleep(4)
    return wifi_connected()

def wifi_connected():
    os.system("ifconfig wlan0 up")
    return check_output("iwgetid wlan0 --raw", shell=True, universal_newlines=True).strip()

@tornado.gen.coroutine
def connect_to_wifi(network_name, password=None):
    result = ''
    if password:
        result = yield connect_private_wifi(network_name, password)
    #else:
    #    result = connect_public_wifi(network_name)
    return result

def split_file_for_print(printrun):
    os.system("split -l 500000 /home/pi/temp/first/pt2.gcode /home/pi/temp/splited/")
    for filename in sorted(os.listdir("/home/pi/temp/splited")):
        gcode = gcoder.LightGCode([i.strip() for i in open("/home/pi/temp/splited/{}".format(filename))])
        printrun.append_gcode(gcode)
    os.system("rm /home/pi/temp/first/pt2.gcode")
    os.system("rm /home/pi/temp/splited/*")

def grouper(iterable, n):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

def split_gcode_for_print(cosa):
    patched_gcode = cosa[0]
    printrun = cosa[1]
    lasts = list(itertools.islice(patched_gcode, 100, len(patched_gcode)))
    grouper_func = grouper(lasts, 500000)
    chuncks = list(grouper_func)
    for chunk in chuncks:
        gcode = gcoder.LightGCode(chunk)
        printrun.append_gcode(gcode)

def get_extruder(extruder):
    if extruder == "ext_1":
        extruder = "T0"
    elif extruder == "ext_2":
        extruder = "T1"
    return extruder

def check_file_print_finished():
    if os.path.exists("/home/pi/print_end_status/end_print"):
        ws = create_connection("ws://127.0.0.1:8888/print-finished")
        ws.send("print_finished")
        ws.close()
        os.system("rm /home/pi/print_end_status/*")

def get_extruder_materials():
    mat_temps = {
           "1" :"ABS",
           "2" :"Flex",
           "3" :"HIPS",
           "4" :"Nylon",
           "5" :"PETG",
           "6" :"PLA Tough",
           "7" :"PLA+",
           "8" :"PVA"
        }
    return mat_temps

def reset_rpi():
    os.system("sudo killall pigpiod")
    os.system("sudo reboot -h now")

def get_sd():
    '''
    Frist get the list of devs and UUID from OS:
    ['/dev/mmcblk0p4: UUID="16231e2a-a5bd-4198-8054-09950ae8e24f"', '/dev/sda1: UUID="ECCD-8D60"', '/dev/sdb1: UUID="F8DF-6CD3"']
    Second give me the list of devs
    [l.split(':', 1)[0].split("/")[-1] for l in info]  ['mmcblk0p4', 'sda1', 'sdb1']
    Third the list of UUID
    [l.split(':', 1)[1].split("=")[-1].replace('"', '') for l in info] ['16231e2a-a5bd-4198-8054-09950ae8e24f', 'ECCD-8D60', 'F8DF-6CD3']
    Finally put all together in a dict
    '''
    info = check_output("sudo blkid -sUUID", shell=True, universal_newlines=True).splitlines()
    return {l.split(':', 1)[1].split("=")[-1].replace('"', '').strip() : l.split(':', 1)[0].split("/")[-1].strip() for l in info if ':' in l}

def get_volume():
    out = check_output("amixer get PCM playback", shell=True, universal_newlines=True)
    regex = r"([\d]+%)"
    return re.findall(regex, out)[0].split("%")[0]

def set_volume(volume):
    os.system("amixer set PCM playback {}%".format(volume))