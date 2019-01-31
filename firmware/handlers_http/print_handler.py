from handlers_http.basic_handler import BasicHandler
from utils import mount_usb, get_gcodes_from_usb

class PrintSelectionHandler(BasicHandler):
    def get(self):
        self.render("printSelection.html", working_on="haciendo nada")

class LocalFilesSelectionHandler(BasicHandler):
    def get(self):
        self.render("print_local_file.html")

class ListingFilesHandler(BasicHandler):
    def get(self, listing_id):
        items = []
        print("listing id: {}".format(listing_id))
        if listing_id == "1":
            try:
                result = mount_usb(self.firmware.hardware_json["board_uuid"])
                print("resultado: {}".format(result))
                items = get_gcodes_from_usb()
            except:
                items = {}
        elif listing_id == "2":
            b = ""
        self.render("listingFiles.html", items=items)

class TemperaturesHandler(BasicHandler):
    def get(self):
        if self.firmware.is_initialized:
            self.firmware.get_temperatures()
        self.write("ok")

class PreviousPrintHandler(BasicHandler):
    def get(self):
        filename = self.get_cookie("filename")
        self.render("previousPrint.html", filename=filename)

class PrintHandler(BasicHandler):
    def get(self):
        self.firmware.start_print(self.get_cookie("file_path"), self.get_cookie("filename"))
        self.render("printing.html", working_on="imprimiendo")

    def post(self):
        file_path = self.get_body_argument("file_path")
        filename = self.get_body_argument("filename")
        self.set_cookie("file_path", file_path)
        self.set_cookie("filename", filename)
        self.write("ok")

class PauseHandler(BasicHandler):
    def get(self):
        self.firmware.pause()
        self.render("index.html", working_on="en pausa")

class ResumeHandler(BasicHandler):
    def get(self):
        self.firmware.resume()
        #MainHandler.broadcast("desde adentro")
        self.render("index.html", working_on="imprimiendo de nuevo")

class CancelHandler(BasicHandler):
    def get(self):
        self.firmware.cancel() 
        self.render("index.html", working_on="cancelado")