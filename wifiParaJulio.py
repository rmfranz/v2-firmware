import os

os.system("sudo mount -o remount,rw /")
os.system("sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /home/pi/")
os.system("sudo chown pi:pi /home/pi/wpa_supplicant.conf")
os.system("sudo rm /etc/wpa_supplicant/wpa_supplicant.conf")
os.system("sudo ln -s /home/pi/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf")
os.system("sudo mount -o remount,ro /")
