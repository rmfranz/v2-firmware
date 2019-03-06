import tornado.web
import tornado.websocket
from tornado.web import RequestHandler
from tornado.options import parse_command_line
import logging
from tornado.ioloop import PeriodicCallback
from periodic_controller import PeriodicController
from cloud_utils import get_auth
from tornado.escape import json_decode, utf8
from tornado.websocket import websocket_connect

def on_message(msg):
    print("el mensaje: {}".format(msg))

class InitHandler(RequestHandler):
    def post(self):
        #registration_code = self.get_body_argument("registration_code")
        data = json_decode(utf8(self.request.body))
        print(data["registration_code"])
        pc = PeriodicCallback(lambda: self.application.periodic_controller.get_auth(data["registration_code"]), 5000)
        if self.application.periodic_controller.auth_token_caller:
            self.application.periodic_controller.stop_auth_token_caller()
        self.application.periodic_controller.set_auth_token_caller(pc)
        self.application.periodic_controller.start_auth_token_caller()
        self.write("ok")

class InitWebsocketsHandler(RequestHandler):
    def get(self):
        if not self.application.periodic_controller.ws_initialized:
            websocket_connect("ws://127.0.0.1:8888/temperatures", 
                on_message_callback=self.application.periodic_controller.on_temp_message)
            websocket_connect("ws://127.0.0.1:8888/heating-bed", 
                on_message_callback=self.application.periodic_controller.on_bed_heating_message)
            websocket_connect("ws://127.0.0.1:8888/heating-nozzle", 
                on_message_callback=self.application.periodic_controller.on_nozzle_heating_message)
            self.application.periodic_controller.ws_initialized = True
        self.write("ok")

class UnregisterHandler(RequestHandler):
    def get(self):
        self.application.periodic_controller.api_caller.stop()
        self.application.periodic_controller.user_conf_json["auth_token"] = ""
        self.application.periodic_controller.write_user_conf_json()
        self.write("ok")

class DisconnectHandler(RequestHandler):
    def get(self):
        self.application.periodic_controller.local_mode_on()
        self.write("ok")

class ReconnectHandler(RequestHandler):
    def get(self):
        self.application.periodic_controller.local_mode_off()
        self.write("ok")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/init", InitHandler),
            (r"/init-websockets", InitWebsocketsHandler),
            (r"/unregister", UnregisterHandler),
            (r"/disconnect", DisconnectHandler),
            (r"/reconnect", ReconnectHandler),
        ]
        #tornado.web.Application.__init__(self, handlers, autoreload=True)
        tornado.web.Application.__init__(self, handlers)
        self.periodic_controller = PeriodicController()

if __name__ == "__main__":
    app = Application()
    parse_command_line()
    app.listen(9000)
    try:
        logging.info('Starting app')
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:        
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('Exit success')