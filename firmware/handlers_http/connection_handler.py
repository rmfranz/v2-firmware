from handlers_http.basic_handler import * 
from utils import scan_wlan, connect_to_wifi

class WifiConnectionHandler(BasicHandler):

    def get(self):
        cosa = scan_wlan()
        print(cosa)
        self.render("listingWifi.html", wifi_list=cosa, selected=None)

    def post(self):
        network_name = self.get_body_argument("network_name")
        password = self.get_body_argument("password", default=None)
        connect_to_wifi(network_name, password)
        self.render("listingWifi.html", wifi_list=scan_wlan(), selected=network_name)

class ConnectivityHandler(BasicHandler):

    def get(self):
        self.render("connectivity.html")