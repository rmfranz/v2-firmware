# This file is part of the Printrun suite.
#
# Printrun is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Printrun is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Printrun.  If not, see <http://www.gnu.org/licenses/>.

from .eventhandler import PrinterEventHandler
from websocket import create_connection

class SampleHandler(PrinterEventHandler):
    '''
    Sample event handler for printcore.
    '''
    
    def __init__(self):
        pass

    def check_origin(self, origin):
        return True

    def open(self):
        print("A client connected.")

    def on_close(self):
        print("A client disconnected")

    def on_message(self, message):
        print("message: {}".format(message))

    def __write(self, field, text = ""):
        print("%-15s - %s" % (field, text))

    def on_init(self):
        self.__write("on_init")
        
    def on_send(self, command, gline):
        self.__write("on_send", command)
    
    def on_recv(self, line):
        if self.are_temperatures(line.strip()):
            self.create_connection_and_send("ws://127.0.0.1:8888/temperatures", line.strip())
        elif self.are_bed_temperatures(line.strip()):
            self.create_connection_and_send("ws://127.0.0.1:8888/heating-bed", line.strip())
        elif self.are_nozzle_temperatures(line.strip()):
            self.create_connection_and_send("ws://127.0.0.1:8888/heating-nozzle", line.strip())
        self.__write("on_recv", line.strip())
    
    def on_connect(self):
        self.__write("on_connect")
        
    def on_disconnect(self):
        self.__write("on_disconnect")
    
    def on_error(self, error):
        self.__write("on_error", error)
        
    def on_online(self):
        self.__write("on_online")
        
    def on_temp(self, line):
        self.__write("on_temp", line)
    
    def on_start(self, resume):
        self.__write("on_start", "true" if resume else "false")
        
    def on_end(self):
        self.__write("on_end")
        
    def on_layerchange(self, layer):
        self.__write("on_layerchange", "%f" % (layer))

    def on_preprintsend(self, gline, index, mainqueue):
        self.__write("on_preprintsend", gline)
    
    def on_printsend(self, gline):
        self.__write("on_printsend", gline)

    def are_temperatures(self, data):
        return "ok" in data and "T0:" in data and "T1:" in data and "B:" in data and "B:" in data
    
    def are_bed_temperatures(self, data):
        return "B:" in data

    def are_nozzle_temperatures(self, data):
        return "T0:" in data

    def create_connection_and_send(self, url, data):
        ws = create_connection(url)
        ws.send(data.strip())
        ws.close()

