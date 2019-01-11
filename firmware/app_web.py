import tornado.ioloop
import tornado.web
import tornado.websocket
from PrintrunMartin.printcore import printcore
from PrintrunMartin import gcoder
from gcodes_loader.gcodes_loading import patch_and_split_gcodes
from utils import mount_usb, get_gcodes_from_usb
from tornado.options import parse_command_line
import logging
import pickle
import os
from tornado.options import define, options

define("template_folder", default="new/", help="Folder to use")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/home", HomeHandler),
            (r"/print", PrintHandler),
            (r"/pausa", PauseHandler),
            (r"/resume", ResumeHandler),
            (r"/cancelar", CancelHandler),
            (r"/temperatures", TemperaturesWsHandler),
            (r"/heating-bed", HeatingBedWsHandler),
            (r"/heating-nozzle", HeatingNozzleWsHandler),
            (r"/get-temperatures", TemperaturesHandler),
            (r"/print-selection", PrintSelectionHandler),
            (r"/local-files-selection", LocalFilesSelectionHandler),
            (r"/listing-files/([0-9]+)", ListingFilesHandler),
            (r"/confirm-print", PreviousPrintHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "/home/pi/test/assets"}),
        ]
        tornado.web.Application.__init__(self, handlers,
                                         autoreload=True)
        self.printrun = printcore('/dev/ttyACM0',115200)


class BasicHandler(tornado.web.RequestHandler):

    def prepare(self):
        self.printrun = self.application.printrun
        
    def get_gcode(self):    
        with open("cosa.gcode", 'rb') as f:
            gcode = pickle.load(f)
        gcode = gcoder.LightGCode(gcode)
        return gcode


class HomeHandler(BasicHandler):
    def get(self):
        self.render(options.template_folder + "index.html", working_on="haciendo nada")

class PrintSelectionHandler(BasicHandler):
    def get(self):
        self.render(options.template_folder + "printSelection.html", working_on="haciendo nada")

class LocalFilesSelectionHandler(BasicHandler):
    def get(self):
        self.render(options.template_folder + "localFilesSelection.html", working_on="haciendo nada")

class ListingFilesHandler(BasicHandler):
    def get(self, listing_id):
        items = []
        print("listing id: {}".format(listing_id))
        if listing_id == "1":
            result = mount_usb()
            print("resultado: {}".format(result))
            items = get_gcodes_from_usb()
        elif listing_id == "2":
            b = ""
        self.render(options.template_folder + "listingFiles.html", items=items)

class TemperaturesHandler(BasicHandler):
    def get(self):
        self.printrun.send_now("M105")
        self.write("ok")

class PreviousPrintHandler(BasicHandler):
    def get(self):
        filename = self.get_cookie("filename")
        self.render(options.template_folder + "previousPrint.html", filename=filename)

class PrintHandler(BasicHandler):
    def get(self):
        #with open("Ext1__PLATough_CableProtector.gcode") as f:
        with open(self.get_cookie("file_path")) as f:
            gcode = gcoder.LightGCode(patch_and_split_gcodes(f))
            self.printrun.startprint(gcode)
            self.render(options.template_folder + "printing.html", working_on="imprimiendo")

    def post(self):
        file_path = self.get_body_argument("file_path")
        filename = self.get_body_argument("filename")
        self.set_cookie("file_path", file_path)
        self.set_cookie("filename", filename)
        self.write("ok")

class PauseHandler(BasicHandler):
    def get(self):
        self.printrun.pause()
        self.render(options.template_folder + "index.html", working_on="en pausa")

class ResumeHandler(BasicHandler):
    def get(self):
        self.printrun.resume()
        #MainHandler.broadcast("desde adentro")
        self.render(options.template_folder + "index.html", working_on="imprimiendo de nuevo")

class CancelHandler(BasicHandler):
    def get(self):
        self.printrun.cancelprint()
        self.printrun.send_now("G28")
        self.printrun.send_now("M104 S0")
        self.printrun.send_now("M140 S0")    
        self.render(options.template_folder + "index.html", working_on="cancelado")

class TemperaturesWsHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        self.connections.add(self)
        logging.info("A client connected.")

    def on_close(self):
        self.connections.remove(self)
        logging.info("A client disconnected")

    def on_message(self, message):
        logging.info("message: {}".format(message))
        [con.write_message(message) for con in self.connections]
    
    @classmethod
    def broadcast(cls, message):
        [con.write_message(message) for con in cls.connections]

class HeatingBedWsHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        self.connections.add(self)
        logging.info("A client connected.")

    def on_close(self):
        self.connections.remove(self)
        logging.info("A client disconnected")

    def on_message(self, message):
        logging.info("message: {}".format(message))
        [con.write_message(message) for con in self.connections]
    
    @classmethod
    def broadcast(cls, message):
        [con.write_message(message) for con in cls.connections]


class HeatingNozzleWsHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        self.connections.add(self)
        logging.info("A client connected.")

    def on_close(self):
        self.connections.remove(self)
        logging.info("A client disconnected")

    def on_message(self, message):
        logging.info("message: {}".format(message))
        [con.write_message(message) for con in self.connections]
    
    @classmethod
    def broadcast(cls, message):
        [con.write_message(message) for con in cls.connections]


if __name__ == "__main__":
    app = Application()
    parse_command_line()
    app.listen(8888)
    #app.printrun = printcore('/dev/ttyACM0',115200)
    try:
        logging.info('Starting app')
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('Exit success')