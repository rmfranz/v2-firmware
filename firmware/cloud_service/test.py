import tornado.web
import tornado.websocket
from tornado.web import RequestHandler
from tornado.options import parse_command_line
import logging
from tornado import httpclient
import json

URL_CLOUD = "https://cloud.3dprinteros.com/apiprinter/v1/kodak/printer/register"

class InitHandler(RequestHandler):
    def get(self):
        http_client = httpclient.HTTPClient()
        headers = {'Content-Type': 'application/json'}
        body = {"VID": "0KDK", "PID": "0001", "SNR": "00000000000000", 
            "mac": "b827ecf9a6b5", "type": "K_PORTRAIT", "version": "",
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

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", InitHandler),
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)

if __name__ == "__main__":
    app = Application()
    parse_command_line()
    app.listen(9001)
    try:
        logging.info('Starting app')
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:        
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('Exit success')