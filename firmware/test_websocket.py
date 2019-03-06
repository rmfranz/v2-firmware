import tornado.web
import tornado.websocket
from tornado.web import RequestHandler
from tornado.options import parse_command_line
import logging
from handlers_websocket.print_ws_handler import *

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/print-finished", PrintFinishedWsHandler),
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)

if __name__ == "__main__":
    app = Application()
    parse_command_line()
    app.listen(8888)
    try:
        logging.info('Starting app')
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:        
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('Exit success')