import tornado.web
import tornado.websocket
from tornado.web import RequestHandler
from tornado.options import parse_command_line
import logging

class InitHandler(RequestHandler):
    def post(self):
        registration_code = self.get_body_argument("registration_code")


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/init", InitHandler),
        ]
        tornado.web.Application.__init__(self, handlers)

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