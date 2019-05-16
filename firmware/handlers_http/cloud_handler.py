from handlers_http.basic_handler import BasicHandler
from tornado import httpclient
import json
from cloud_service.cloud_utils import cloud_service_resp
import tornado

URL_CLOUD = "https://cloud.3dprinteros.com/apiprinter/v1/kodak/printer/register"
URL_QUEUE = "https://cloud.3dprinteros.com/apiprinter/v1/kodak/printer/get_queued_jobs"
URL_QUEUE_START = "https://cloud.3dprinteros.com/apiprinter/v1/kodak/printer/start_queued_job"

class ToCloudHandler(BasicHandler):
    def get(self):
        if not self.wizzard.viewed:
            async_http_client = httpclient.AsyncHTTPClient()
            async_http_client.fetch("http://127.0.0.1:9000/init-websockets")
        if self.firmware.user_conf_json["auth_token"]:
            self.render("cloud.html", connected=True, cloud_pref=self.firmware.user_conf_json["cloud_pref"], wizzard_viewed=self.wizzard.viewed)
        else:
            self.render("cloud.html", connected=False, cloud_pref=None, wizzard_viewed=self.wizzard.viewed)

class GetRegistrationCodeHandler(BasicHandler):
    def get(self):
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
            #self.render("cloud.html", registration_code=registration_code, cloud_pref=None, wizzard_viewed=self.wizzard.viewed)
            self.write({"registration_code": registration_code})
        else:
            #self.render("cloud.html", registration_code="Error on API", cloud_pref=None, wizzard_viewed=self.wizzard.viewed)
            self.write({"registration_code": "Error"})

class UnregisterHandler(BasicHandler):
    def get(self):
        async_http_client = httpclient.AsyncHTTPClient()
        async_http_client.fetch("http://127.0.0.1:9000/unregister", method='GET', raise_error=False, callback=cloud_service_resp)
        self.firmware.user_conf_json["auth_token"] = ""
        self.firmware.user_conf_json["cloud_pref"] = "disconnected"
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

class ToQueueHandler(BasicHandler):
    def get(self):
        with open("/home/pi/config-files/user_conf.json") as f:
            user_conf_json = json.load(f)
        if user_conf_json["auth_token"]:
            self.render("listing_cloud.html")
        else:
            self.redirect("/to-cloud")

class GetQueueHandler(BasicHandler):
    @tornado.gen.coroutine
    def get(self):
        with open("/home/pi/config-files/user_conf.json") as f:
            user_conf_json = json.load(f)
        async_http_client = httpclient.AsyncHTTPClient()
        resp = yield async_http_client.fetch(URL_QUEUE, method='POST', raise_error=False,
                headers={'Content-Type': 'application/json'}, 
                body=json.dumps({"auth_token": user_conf_json["auth_token"]}))
        if resp.code == 200:
            self.write({"resp": json.loads(resp.body.decode('utf-8'))})
        else:
            self.write({"resp":"error"})

class ToConfirmPrintHandler(BasicHandler):
    @tornado.gen.coroutine
    def get(self):
        error = None
        cloud_job = None
        job_id = self.get_argument("job_id")
        with open("/home/pi/config-files/user_conf.json") as f:
            user_conf_json = json.load(f)
        async_http_client = httpclient.AsyncHTTPClient()
        resp = yield async_http_client.fetch(URL_QUEUE, method='POST', raise_error=False,
                headers={'Content-Type': 'application/json'}, 
                body=json.dumps({"auth_token": user_conf_json["auth_token"]}))
        if resp.code == 200:
            jobs = json.loads(resp.body.decode('utf-8'))
            for job in jobs:
                if job["id"] == job_id:
                    cloud_job = job
            if not cloud_job:
                error = "error"
        else:
            error = "error"
        time = float(cloud_job["printing_duration"])
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        self.render("previous_cloud_print.html", error=error, cloud_job=cloud_job, hours=int(hour), minutes=int(minutes))

class PrintCloudHandler(BasicHandler):
    @tornado.gen.coroutine
    def get(self):
        job_id = self.get_argument("job_id")
        with open("/home/pi/config-files/user_conf.json") as f:
            user_conf_json = json.load(f)
        async_http_client = httpclient.AsyncHTTPClient()
        resp = yield async_http_client.fetch(URL_QUEUE_START, method='POST', raise_error=False,
                headers={'Content-Type': 'application/json'}, 
                body=json.dumps({"auth_token": user_conf_json["auth_token"], "job_id": job_id}))
        if resp.code == 200:
            self.render("phantom.html", error=None)
        else:
            self.render("phantom.html", error="error")

class SetUserCloudHanlder(BasicHandler):
    def post(self):
        status = self.get_body_argument("status")
        if status == "connected":
            self.firmware.refresh_user_conf()
        self.write("ok")