from handlers_http.basic_handler import BasicHandler
from tornado import httpclient
import json
from cloud_service.cloud_utils import cloud_service_resp

URL_CLOUD = "https://cloud.3dprinteros.com/apiprinter/v1/kodak/printer/register"

class GetRegistrationCodeHandler(BasicHandler):
    def get(self):
        if self.firmware.user_conf_json["auth_token"]:
            self.render("cloud.html", registration_code=None, cloud_pref=self.firmware.user_conf_json["cloud_pref"], wizzard_viewed=self.wizzard.viewed)
        else:
            headers = {'Content-Type': 'application/json'}
            body = {"VID": "0KDK", "PID": "0001", "SNR": self.firmware.hardware_json["serial_number"], 
                "mac": self.firmware.get_macaddress().replace(":", ""), "type": "K_PORTRAIT", "version": "",
                "registration_code_ttl": 20}
            http_client = httpclient.HTTPClient()
            resp = http_client.fetch(URL_CLOUD, method='POST', raise_error=False,
                    headers=headers, body=json.dumps(body))
            if resp.code == 200:
                resp_dict = json.loads(resp.body.decode('utf-8'))
                registration_code = resp_dict["registration_code"]
                async_http_client = httpclient.AsyncHTTPClient()
                async_http_client.fetch("http://127.0.0.1:9000/init", method='POST', raise_error=False,
                    headers=headers, body=json.dumps({"registration_code": registration_code}), callback=cloud_service_resp)
                self.render("cloud.html", registration_code=registration_code, cloud_pref=None, wizzard_viewed=self.wizzard.viewed)
            else:
                self.render("cloud.html", registration_code="Error on API", cloud_pref=None, wizzard_viewed=self.wizzard.viewed)

class UnregisterHandler(BasicHandler):
    def get(self):
        async_http_client = httpclient.AsyncHTTPClient()
        async_http_client.fetch("http://127.0.0.1:9000/unregister", method='GET', raise_error=False, callback=cloud_service_resp)
        self.firmware.user_conf_json["auth_token"] = ""
        self.firmware.write_user_conf()
        self.redirect("/to-cloud")

class DisconnectHandler(BasicHandler):
    def get(self):
        self.firmware.user_conf_json["cloud_pref"] = "disconnected"
        self.firmware.write_user_conf()
        async_http_client = httpclient.AsyncHTTPClient()
        async_http_client.fetch("http://127.0.0.1:9000/disconnect", method='GET', raise_error=False, callback=cloud_service_resp)
        self.redirect("/to-cloud")

class ReconnectHandler(BasicHandler):
    def get(self):
        self.firmware.user_conf_json["cloud_pref"] = "connected"
        self.firmware.write_user_conf()
        async_http_client = httpclient.AsyncHTTPClient()
        async_http_client.fetch("http://127.0.0.1:9000/reconnect", method='GET', raise_error=False, callback=cloud_service_resp)
        self.redirect("/to-cloud")

class SetUserCloudHanlder(BasicHandler):
    def post(self):
        status = self.get_body_argument("status")
        if status == "connected":
            self.firmware.refresh_user_conf()
        self.write("ok")