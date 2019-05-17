import tornado.web
import tornado.websocket
from tornado.web import RequestHandler
from tornado.options import parse_command_line
import logging
from tornado import httpclient
import json

URL_CLOUD = "https://kodak-dev-acorn.3dprinteros.com/apiprinter/v1/kodak/printer/register"
URL_QUEUE = "https://kodak-dev-acorn.3dprinteros.com/apiprinter/v1/kodak/printer/get_queued_jobs"
AUTH = "L2bEH2GI7W5YUcRewoXbXWr82Z7LwaNOJgsmAeZVponydTOkaOq3rWOdwhgAAgvMNkZTmNRxjSMMp5R1IvZ1eTPPLUJJjlvDMWuERYqss7FBijngsOZy9TSwkIn2I4Qq"

class InitHandler(RequestHandler):
    def get(self):
        http_client = httpclient.HTTPClient()
        headers = {'Content-Type': 'application/json'}
        body = {"VID": "0KDK", "PID": "0001", "SNR": "00000000000000", 
            "mac": "b797ecf9a6b5", "type": "K_PORTRAIT", "version": "",
            "registration_code_ttl": 20}
        http_client = httpclient.HTTPClient()
        resp = http_client.fetch(URL_CLOUD, method='POST', raise_error=False,
                headers=headers, body=json.dumps(body))
        resp_dict = json.loads(resp.body.decode('utf-8'))
        if resp.code == 200:
            body = {"registration_code": resp_dict["registration_code"]}
            print("mando")
            print(body)
            resp_reg = http_client.fetch("http://localhost:9000/init", method='POST', raise_error=False, headers=headers, body=json.dumps(body))
            print(resp_reg.body)
            self.write("oik")
        else:
            print(resp_dict)
            self.write("no ok")

def cloud_service_resp(re):
    print(re)

class GetRegistrationCodeHandler(RequestHandler):
    def get(self):
        headers = {'Content-Type': 'application/json'}
        body = {"auth_token": AUTH}
        http_client = httpclient.HTTPClient()
        resp = http_client.fetch(URL_QUEUE, method='POST', raise_error=False,
                headers=headers, body=json.dumps(body))
        if resp.code == 200:
            resp_dict = json.loads(resp.body.decode('utf-8'))
            print(resp_dict)
            #body = {"registration_code": resp_dict["registration_code"]}
            #async_http_client = httpclient.AsyncHTTPClient()
            #async_http_client.fetch("http://127.0.0.1:9000/init", method='POST', raise_error=False,
            #    headers=headers, body=json.dumps(body), callback=cloud_service_resp)
            self.write("ok")
        else:
            resp_dict = json.loads(resp.body.decode('utf-8'))
            print(resp_dict)
            self.write("ok")

class TranslationHandler(RequestHandler):
    def get(self):
        print(self.locale.translate("calibration_error"))
        self.render("index.html", lights_on="true")
    
    def get_user_locale(self):
        #with open("user_conf.json") as f:
        #    cosa = json.load(f)
        return tornado.locale.get("eng")
        
class CosaHandler(RequestHandler):
    def post(self):
        file_path = self.get_body_argument("file_path")
        print(file_path)
        try:
            filename = self.get_body_argument("filename").split(".gcode")[0]
        except:
            filename = self.get_body_argument("filename")
        print(filename)
        self.write("ok")

    def get(self):
        self.write({"sme": "text"})

class AlgoHandler(RequestHandler):
    def get(self):
        l = [5,6,5,343,7,45,6,7,78,8,86,5,4]
        self.write(str(len(l)))

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", GetRegistrationCodeHandler),
            (r"/translation", TranslationHandler),
            (r"/cosa", CosaHandler)
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True, template_path="../templates/")

if __name__ == "__main__":
    app = Application()
    parse_command_line()
    tornado.locale.load_translations("../../translations")
    app.listen(9001)
    try:
        logging.info('Starting app')
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:        
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('Exit success')