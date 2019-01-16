from handlers_http.basic_handler import BasicHandler
from tornado.options import define, options
from utils import mount_usb, get_gcodes_from_usb
from gcodes_loader.gcodes_loading import patch_and_split_gcodes
from printcore_modified import gcoder

define("template_folder", default="templates/", help="Folder to use")

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