from handlers_http.basic_handler import * 
from utils import scan_wlan, connect_to_wifi, wifi_connected
import tornado

class WifiConnectionHandler(BasicHandler):

    @concurrent.run_on_executor
    def get(self):
        wifi_list = scan_wlan()
        selected = wifi_connected()
        #self.render("listing_wifi.html", wifi_list=wifi_list, selected=selected, wizzard_viewed=self.wizzard.viewed)
        self.write({"wifi_list": wifi_list, 'selected': selected})

class ToWifiConnectionHandler(BasicHandler):

    def get(self):
        self.render("listing_wifi.html", wizzard_viewed=self.wizzard.viewed)

    @tornado.gen.coroutine
    def post(self):
        network_name = self.get_body_argument("network_name")
        password = self.get_body_argument("password", default=None)
        result = yield connect_to_wifi(network_name, password)
        #self.render("listing_wifi.html", wifi_list=scan_wlan(), selected=network_name)
        if not result or network_name == result:
            result = self.locale.translate("network_connect_failure")
        self.write(result)

class ConnectivityHandler(BasicHandler):

    def get(self):
        self.render("connectivity.html")