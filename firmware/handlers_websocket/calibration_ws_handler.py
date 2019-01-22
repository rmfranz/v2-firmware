import logging
from tornado.websocket import WebSocketHandler

class ZProbeWsHandler(WebSocketHandler):
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

class ProbeCompleteWsHandler(WebSocketHandler):
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