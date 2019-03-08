from tornado import httpclient
import json
from tornado.ioloop import PeriodicCallback
import tornado
import os
from tornado.websocket import websocket_connect
import asyncio
import functools

class PeriodicController:

    HARDWARE_JSON_FOLDER = "/home/pi/config-files/hardware.json"
    USER_CONF_JSON_FOLDER = "/home/pi/config-files/user_conf.json"

    def __init__(self):
        with open(self.HARDWARE_JSON_FOLDER) as f:
            self.hardware_json = json.load(f)
        with open(self.USER_CONF_JSON_FOLDER) as f:
            self.user_conf_json = json.load(f)
        self.auth_token_caller = None
        self.t0 = 24
        self.t1 = 24
        self.bed = 24
        self.amber = 24
        self.t0_target = 0
        self.t1_target = 0
        self.bed_target = 0
        self.amber_target = 0
        self.url_cloud = "https://cloud.3dprinteros.com/apiprinter/v1/kodak/printer/register"
        self.url_command = "https://cloud.3dprinteros.com/apiprinter/v1/kodak/printer/command"
        self.auth_token = self.user_conf_json["auth_token"]
        self.api_caller = PeriodicCallback(self.command_request, 2000)
        self.state = "ready"
        self.headers = {'Content-Type': 'application/json'}
        self.commander = {
            "gcodes": self.on_print,
            "pause": self.on_pause,
            "unpause": self.on_resume,
            "cancel": self.on_cancel
        }
        self.ws_url = "ws://127.0.0.1:8888/cloud"
        self.ws_initialized = False
        if self.auth_token:
            self.api_caller.start()


    def set_auth_token_caller(self, caller):
        self.auth_token_caller = caller

    def start_auth_token_caller(self):
        self.auth_token_caller.start()

    def stop_auth_token_caller(self):
        self.auth_token_caller.stop()

    @tornado.gen.coroutine
    def get_auth(self, registration_code):        
        body_with_registration = {"VID": "0KDK", "PID": "0001", "SNR": "00000000000000",
            "mac": self.hardware_json["mac_address_eth0"].replace(":", ""), "type": "K_PORTRAIT",  "version": "", 
            "registration_code_ttl": 20,  "registration_code": registration_code}
        request = httpclient.HTTPRequest(url=self.url_cloud, method='POST',
                    headers=self.headers, body=json.dumps(body_with_registration))
        async_http_client = httpclient.AsyncHTTPClient()
        #async_http_client.fetch(request, self.on_done_auth, raise_error=False)
        response = yield async_http_client.fetch(request, raise_error=False)
        resp_dict = json.loads(response.body.decode('utf-8'))
        if response.code == 200 and "auth_token" in resp_dict:
            self.auth_token = resp_dict["auth_token"]
            self.user_conf_json["auth_token"] = resp_dict["auth_token"]
            self.write_user_conf_json()
            self.stop_auth_token_caller()
            self.api_caller.start()
            self.create_connection_and_send("connected")
        else:
            print("There is nothing: {}".format(resp_dict))

    def on_done_auth(self, response):
        resp_dict = json.loads(response.body.decode('utf-8'))
        if response.code == 200 and "auth_token" in resp_dict:
            self.auth_token = resp_dict["auth_token"]
            self.hardware_json["auth_token"] = resp_dict["auth_token"]
            self.write_hardware_json()
            self.stop_auth_token_caller()
            self.api_caller.start()
            self.create_connection_and_send("connected")
        else:
            print("There is nothing: {}".format(resp_dict))

    @tornado.gen.coroutine
    def command_request(self):
        req = {
            "report": {
            "state": self.state,
            "percent": "0",
            "temps": [self.bed, self.t1, self.t0, "c" + str(self.amber)],
            "target_temps": [self.bed_target, self.t1_target, self.t0_target],
            "fan_speeds": ["0", "0"]
            },
            "auth_token": self.auth_token
        }
        async_http_client = httpclient.AsyncHTTPClient()
        resp_reg = yield async_http_client.fetch(self.url_command, method='POST', raise_error=False,
                    headers=self.headers, body=json.dumps(req))
        resp_dict = json.loads(resp_reg.body.decode('utf-8'))
        print(resp_dict)
        if "command" in resp_dict:
            self.commander[resp_dict["command"]](resp_dict)

    def on_print(self, resp_dict):
        self.state = "downloading"
        request = httpclient.HTTPRequest(url=resp_dict["payload"], streaming_callback=self.on_chunk,
                    request_timeout=3600)
        async_http_client = httpclient.AsyncHTTPClient()
        async_http_client.fetch(request, self.on_download_done)
        self.create_connection_and_send("gcodes")
        
    def on_pause(self, resp_dict):
        self.state = "paused"
        self.create_connection_and_send("pause")

    def on_resume(self, resp_dict):
        self.state = "printing"
        self.create_connection_and_send("unpause")

    def on_cancel(self, resp_dict):
        os.remove("/home/pi/cloud/cloud.gcode")
        self.state = "ready"
        self.create_connection_and_send("cancel")

    def on_chunk(self, chunk):
        with open("/home/pi/cloud/cloud.gcode", "ab+") as f:
            f.write(chunk)

    def on_download_done(self, response):
        self.state = "printing"
        self.create_connection_and_send("download_done")

    def on_temp_message(self, msg):
        temps = msg.split("@")
        self.set_temps(
            temps[0][temps[0].index(":") + 1 : temps[0].index("/")].strip(),
            temps[1][temps[1].index(":") + 1 : temps[1].index("/")].strip(),
            temps[2][temps[2].index(":") + 1 : temps[2].index("/")].strip(),
            temps[3][temps[3].index(":") + 1 : temps[3].index("/")].strip()
        )
        self.set_target_temps(
            temps[0][temps[0].index("/") + 1 :].strip(),
            temps[1][temps[1].index("/") + 1 :].strip(),
            temps[2][temps[2].index("/") + 1 :].strip(),
            temps[3][temps[3].index("/") + 1 :].strip()
        )

    def on_bed_heating_message(self, msg):
        self.bed = msg[msg.index(":") + 1 : msg.index("/")].strip()
        self.bed_target = msg[msg.index("/") + 1 : msg.index("@")].strip()

    def on_nozzle_heating_message(self, msg):
        temp = msg[msg.index(":") + 1 : msg.index("/")].strip()
        nozzle_type = msg[msg.index("T") + 1 : msg.index(":")].strip()
        target = msg[msg.index("/") + 1 : msg.index("@")].strip()
        if nozzle_type == '0':
            self.t0 = temp
            self.t0_target = target
        elif nozzle_type == '1':
            self.t1 = temp
            self.t1_target = target

    def set_temps(self, t0, t1, bed, amber):
        self.t0 = t0
        self.t1 = t1
        self.bed = bed
        self.amber = amber

    def set_target_temps(self, t0_target, t1_target, bed_target, amber_target):
        self.t0_target = t0_target
        self.t1_target = t1_target
        self.bed_target = bed_target
        self.amber_target = amber_target

    def local_mode_on(self):
        self.state = "local_mode"

    def local_mode_off(self):
        self.state = "ready"

    def create_connection_and_send(self, data):
        tornado.ioloop.IOLoop().run_sync(functools.partial(self.create_connection_and_send_async, data))
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #loop.run_until_complete( self.create_connection_and_send_async(data))
        #loop.close()

    @tornado.gen.coroutine
    def create_connection_and_send_async(self, data):
        ws = yield websocket_connect(self.ws_url)
        ws.write_message(data.strip())
        ws.close()

    def write_hardware_json(self):
        with open(self.HARDWARE_JSON_FOLDER, 'w') as f:
                json.dump(self.hardware_json, f)

    def write_user_conf_json(self):
        with open(self.USER_CONF_JSON_FOLDER, 'w') as f:
                json.dump(self.user_conf_json, f)