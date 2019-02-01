import os, fnmatch
from subprocess import check_output, call
from printcore_modified import gcoder
import itertools

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

def connect_private_wifi(network_name, password):
    network_number = int(check_output("wpa_cli add_network | grep -v \"Selected interface 'p2p-dev-wlan0'\"", shell=True, universal_newlines=True))
    os.system("sudo mount -o remount,rw /")
    os.system("sudo wpa_cli set_network {} ssid '\"{}\"'".format(network_number, network_name))
    os.system("sudo wpa_cli set_network {} psk '\"{}\"'".format(network_number, password))
    os.system("sudo wpa_cli enable_network {}".format(network_number))
    os.system("sudo wpa_cli select_network {}".format(network_number))
    os.system("sudo wpa_cli save_config")
    os.system("sudo wpa_cli -i wlan0 reconfigure")
    os.system("sudo mount -o remount,ro /")

def connect_to_wifi(network_name, password=None):
    if password:
        connect_private_wifi(network_name, password)
    else:
        connect_public_wifi(network_name)

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