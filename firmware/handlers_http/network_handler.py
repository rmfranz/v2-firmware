from handlers_http.basic_handler import BasicHandler
from urllib.request import urlopen
from subprocess import check_output
import os

class ToInfoHandler(BasicHandler):
    def get(self):
        try:
            ip_public = urlopen('http://ip.42.pl/raw').read()
        except:
            ip_public = ""
        ip_local = check_output("hostname -I", shell=True, universal_newlines=True).strip()
        self.render("info.html", ip_public=ip_public, ip_local=ip_local, ssh=self.get_cookie("ssh", default="disable"))

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