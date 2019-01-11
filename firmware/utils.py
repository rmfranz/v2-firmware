import os, fnmatch

def mount_usb():
    return os.system("sudo mount /dev/sda1 /media/usb -o uid=pi,gid=pi")

def get_gcodes_from_usb():
    dirName = "/media/usb"
    pattern = "*.gcode"
    dict_of_files = {}
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        dict_of_files.update({file: os.path.join(dirpath, file) for file in filenames if fnmatch.fnmatch(file, pattern)})
    return dict_of_files