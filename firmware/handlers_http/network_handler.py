from handlers_http.basic_handler import BasicHandler
from urllib.request import urlopen
from subprocess import check_output
import os

class ToNetworkInfoHandler(BasicHandler):
    def get(self):
        wifi_command = ''' ifconfig wlan0 | grep "inet " | awk -F'[: ]+' '{ print $3 }' '''
        eth_command = ''' ifconfig eth0 | grep "inet " | awk -F'[: ]+' '{ print $3 }' '''
        ip_wifi = check_output(wifi_command, shell=True, universal_newlines=True).strip()
        ip_eth = check_output(eth_command, shell=True, universal_newlines=True).strip()
        self.render("network_info.html", ip_wifi=ip_wifi, ip_eth=ip_eth, ssh=self.get_cookie("ssh", default="disable"))

class EnableSSHHandler(BasicHandler):
    def get(self):
        os.system("sudo systemctl enable ssh")
        os.system("sudo systemctl start ssh")
        self.set_cookie("ssh", "enable")
        self.redirect("/network-info")

class DisableSSHHandler(BasicHandler):
    def get(self):
        os.system("sudo systemctl stop ssh")
        os.system("sudo systemctl disable ssh")
        self.set_cookie("ssh", "disable")
        self.redirect("/network-info")