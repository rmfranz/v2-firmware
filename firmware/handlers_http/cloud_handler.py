from handlers_http.basic_handler import BasicHandler
from tornado import httpclient
import json

URL_CLOUD = "https://cloud.3dprinteros.com/apiprinter/v1/kodak/printer/register"

class GetRegistrationCodeHandler(BasicHandler):
    def get(self):
        headers = {'Content-Type': 'application/json'}
        body = {"VID": "0KDK", "PID": "0001", "SNR": "00000000000000", 
            "mac": self.firmware.get_macaddress(), "type": "K_PORTRAIT", "version": "",
            "registration_code_ttl": 20}
        http_client = httpclient.HTTPClient()
        resp = http_client.fetch(URL_CLOUD, method='POST', raise_error=False,
                headers=headers, body=json.dumps(body))
        if resp.code == 200:
            resp_dict = json.loads(resp.body.decode('utf-8'))
            registration_code = resp_dict["registration_code"]
            async_http_client = httpclient.AsyncHTTPClient()
            async_http_client.fetch("http://127.0.0.1:9000/init", method='POST', raise_error=False,
                headers=headers, body=json.dumps(body))
            self.render("cloud.html", registration_code=registration_code)
        else:
            self.render("cloud.html", registration_code="Error on API")