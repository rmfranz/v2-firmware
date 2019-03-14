from handlers_http.basic_handler import BasicHandler
from utils import mount_usb, get_gcodes_from_usb, get_gcodes_from_sample, get_gcodes_from_calibration
import tornado
from tornado import httpclient
import os

class PrintSelectionHandler(BasicHandler):
    def get(self):
        self.render("print_selection.html")

class LocalFilesSelectionHandler(BasicHandler):
    def get(self):
        self.render("print_local_file.html")

class ListingFilesHandler(BasicHandler):
    def get(self, listing_id):
        """
            When listing:
                1 -> usb
                2 -> samples
                3 -> calibration    
        """
        items = []
        if listing_id == "1":
            try:
                result = mount_usb(self.firmware.hardware_json["board_uuid"])
                print("resultado: {}".format(result))
                if result == 0:
                    items = get_gcodes_from_usb()                    
                else:
                    items = {}
                    error = "No se pudo montar el usb"
            except:
                items = {}
        elif listing_id == "2":
           items = get_gcodes_from_sample()
        elif listing_id == "3":
           items = get_gcodes_from_calibration()
        if not items:
            error = "error"
        else:
            error = ""
        self.render("listing_files.html", items=items, error=error)

class TemperaturesHandler(BasicHandler):
    def get(self):
        if self.firmware.is_initialized:
            self.firmware.get_temperatures()
        self.write("ok")

class PreviousPrintHandler(BasicHandler):
    def get(self):
        filename = self.firmware.filename
        self.render("previous_print.html", filename=filename)

class PrintHandler(BasicHandler):
    def get(self):
        if os.path.exists(self.firmware.file_path):
            self.firmware.start_print()
            #self.print_finished_controller.start()
            #http_client = httpclient.HTTPClient()
            #resp_reg = http_client.fetch("http://127.0.0.1:9000/init-print", method='GET', raise_error=False)
            #print(resp_reg.body.decode('utf-8'))
            self.render("printing.html", filename=self.firmware.filename)
        else:
            self.render("listing_files.html", items=[], error="error")

    def post(self):
        file_path = self.get_body_argument("file_path")
        try:
            filename = self.get_body_argument("filename").split(".gcode")[0]
        except:
            filename = self.get_body_argument("filename")
        self.firmware.set_file_to_print(file_path, filename)
        self.write("ok")

class PrintNowHandler(BasicHandler):
    def get(self):
        self.firmware.start_print()
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
        #self.render("index.html", working_on="cancelado")
        self.write("ok")

class CancelCloudHandler(BasicHandler):
    def get(self):
        self.firmware.cancel()
        self.redirect("/home")

class PrintFinishedHandler(BasicHandler):
    def get(self):
        time_printing = self.get_cookie("time_printing")
        self.render("print_finished.html", filename=self.firmware.filename, time_printing=time_printing)

    def post(self):
        time_printing = self.get_body_argument("time_printing")
        self.set_cookie("time_printing", time_printing)
        self.write("ok")

class GetTotalLinesHandler(BasicHandler):
    def get(self):
        self.write(str(self.firmware.total_lines))

class GetNumLineHandler(BasicHandler):
    def get(self):
        self.write(str(self.firmware.the_counter.count_lines()))

class GetPercentage(BasicHandler):
    def get(self):
        try:
            percentage = (self.firmware.the_counter.count_lines() * 100) / self.firmware.totalLines
        except:
            percentage = 0
        self.write(str(percentage))

class TestHandler(BasicHandler):
    def get(self):
        print("me pegaron")
        self.write("ok")