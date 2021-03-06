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
            websocket_connect("ws://127.0.0.1:8888/print-finished", 
                on_message_callback=self.application.periodic_controller.on_finish_print)
            self.application.periodic_controller.ws_initialized = True
        self.write("ok")

class UnregisterHandler(RequestHandler):
    def get(self):
        self.application.periodic_controller.api_caller.stop()
        self.write("ok")

class DisconnectHandler(RequestHandler):
    def get(self):
        self.application.periodic_controller.local_mode_on()
        self.write("ok")

class SetPauseHandler(RequestHandler):
    def get(self):
        self.application.periodic_controller.set_pause()
        self.write("ok")

class SetResumeHandler(RequestHandler):
    def get(self):
        self.application.periodic_controller.set_resume()
        self.write("ok")

class SetCancelHandler(RequestHandler):
    def get(self):
        self.application.periodic_controller.set_cancel()
        self.write("ok")

class ReconnectHandler(RequestHandler):
    def get(self):
        self.application.periodic_controller.local_mode_off()
        self.write("ok")

class SetSerialHandler(RequestHandler):
    def post(self):
        data = json_decode(utf8(self.request.body))
        self.application.periodic_controller.set_serial(data["serial"])
        self.write("ok")

class LocalPrintingHandler(RequestHandler):
    def get(self):
        print_local = int(self.get_argument('print_local', 0))
        if print_local == 0:
            self.application.periodic_controller.print_local_off()
        elif print_local == 1:
            self.application.periodic_controller.print_local_on()
        self.write("ok")

class RefreshHardwareHandler(RequestHandler):
    def get(self):
        self.application.periodic_controller.refresh_hardware_json()
        self.application.periodic_controller.refresh_user_conf_json()
        self.write("ok")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/init", InitHandler),
            (r"/init-websockets", InitWebsocketsHandler),
            (r"/unregister", UnregisterHandler),
            (r"/disconnect", DisconnectHandler),
            (r"/reconnect", ReconnectHandler),
            (r"/set-serial", SetSerialHandler),
            (r"/refresh", RefreshHardwareHandler),
            (r"/local-printing", LocalPrintingHandler),
            (r"/set-pause", SetPauseHandler),
            (r"/set-resume", SetResumeHandler),
            (r"/set-cancel", SetCancelHandler)
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