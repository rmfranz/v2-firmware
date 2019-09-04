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
import os
from tornado.websocket import websocket_connect
import tornado
import asyncio
import functools
import logging
import traceback

class SmoothieHandler(PrinterEventHandler):
    '''
    Sample event handler for printcore.
    '''
    
    def __init__(self):
        self.printing = False
        self.paused = False
        self.in_error = False
        self.the_counter = None
        self.ioloop = tornado.ioloop.IOLoop(make_current=False)
        self.smoothie_logger = logging.getLogger('smoothie_logger')
        self.board_logger = logging.getLogger('board_logger')
        
    def check_origin(self, origin):
        return True

    def set_the_counter(self, the_counter):
        self.the_counter = the_counter

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
        elif self.is_z_probe_triggered(line.strip()):
            self.create_connection_and_send("ws://127.0.0.1:8888/z-probe", line.strip())
        elif self.is_probe_complete(line.strip()):
            self.create_connection_and_send("ws://127.0.0.1:8888/probe-complete", line.strip())
        elif self.is_probe_failed(line.strip()):
            self.create_connection_and_send("ws://127.0.0.1:8888/probe-failed", line.strip())
        elif self.is_for_grid(line.strip()):
            self.create_connection_and_send("ws://127.0.0.1:8888/inspect-grid", line.strip())
        else:
            if line.strip() != 'ok':
                ln_num = 0
                if self.the_counter:
                    ln_num = self.the_counter.count_lines()
                self.smoothie_logger.debug(str(ln_num) + " - " + str(line.strip()))
        if self.is_error(line.strip()) and not self.in_error:
            self.create_connection_and_send("ws://127.0.0.1:8888/error-handler", "ERR002")
            self.in_error = True
            self.board_logger.error(line.strip())
        self.__write("on_recv", line.strip())
    
    def on_connect(self):
        self.__write("on_connect")
        
    def on_disconnect(self):
        self.__write("on_disconnect")
    
    def on_error(self, error):
        if not self.in_error:
            self.create_connection_and_send("ws://127.0.0.1:8888/error-handler", "ERR001")
        self.smoothie_logger.debug(error.strip())
        self.board_logger.error(error.strip())
        self.in_error = True
        self.__write("on_error", error)
        
    def on_online(self):
        self.__write("on_online")
        
    def on_temp(self, line):
        self.__write("on_temp", line)
    
    def on_start(self, resume):
        self.printing = True
        self.__write("on_start", "true" if resume else "false")
        
    def on_end(self):      
        if not self.paused:
            self.create_connection_and_send("ws://127.0.0.1:8888/print-finished", "print_finished")
            self.printing = False
            self.the_counter.remove_lines()
        #    os.system("sudo touch /home/pi/print_end_status/end_print")
        self.__write("on_end")
        
    def on_layerchange(self, layer):
        self.__write("on_layerchange", "%f" % (layer))

    def on_preprintsend(self, gline, index, mainqueue):
        self.__write("on_preprintsend", gline)
    
    def on_printsend(self, gline):
        self.the_counter.add_line(gline)
        #if self.printing:
        #    self.create_connection_and_send("ws://127.0.0.1:8888/line-sended", gline.strip())
        self.__write("on_printsend", gline)

    def on_pause(self):
        self.paused = True

    def on_resume(self):
        self.paused = False

    def on_cancel(self):
        self.paused = False
        self.printing = False
        self.the_counter.remove_lines()

    def are_temperatures(self, data):
        return "ok" in data and "T0:" in data and "T1:" in data and "B:" in data and "A:" in data
    
    def are_bed_temperatures(self, data):
        return "B:" in data and "T0:" not in data and "T1:" not in data and "A:" not in data

    def are_nozzle_temperatures(self, data):
        return ("T0:" in data or "T1:" in data) and ("B:" not in data and "A:" not in data)

    def is_z_probe_triggered(self, data):
        return "Z:" in data

    def is_probe_complete(self, data):
        return "Probe completed" in data

    def is_probe_failed(self, data):
        return "Probe failed" in data

    def is_for_grid(self, data):
        list_item = data.split(" ")
        return len(list_item) == 5 and (self.is_numeric(list_item[0]) or list_item[0] == "nan")

    def is_numeric(self, s):
        try:
            float(s)
            return True
        except (ValueError, TypeError):
            return False

    def is_error(self, data):
        return "ERROR" in data or "!!" in data or "HALT" in data
    
    def create_connection_and_send(self, url, data):
        try:
            self.ioloop.run_sync(functools.partial(self.create_connection_and_send_async, url, data))
        except Exception:
            self.smoothie_logger.error(str(traceback.format_exc()))
            self.board_logger.error(str(traceback.format_exc()))
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #loop.run_until_complete( self.create_connection_and_send_async(url, data))
        #loop.close()

    @tornado.gen.coroutine
    def create_connection_and_send_async(self, url, data):
        try:
            ws = yield websocket_connect(url)
            ws.write_message(data.strip())
        except Exception:
            self.smoothie_logger.error(str(traceback.format_exc()))
            self.board_logger.error(str(traceback.format_exc()))
        finally:
            ws.close()

