"""Application main entry point for our tornado app"""
import os
import sys
import tornado.ioloop
import tornado.web

from tornado import template

# Template loader
TPL_PATH = os.path.join(os.path.dirname(__file__), 'tpl')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

from bookie_parser.logconfig import LOG
from bookie_parser.handlers import MainHandler
from bookie_parser.handlers import ReadableHandler
from bookie_parser.handlers import ViewableHandler


application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/readable/(.*)", ReadableHandler),
        (r"/view/(.*)", ViewableHandler),
        (r"/view", ViewableHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler,
            {"path": STATIC_PATH}),
    ],
    static_path=STATIC_PATH,
    template_path=TPL_PATH,
    )


def main(host='0.0.0.0', port=5000):
    LOG.info('starting server on port: ' + str(port))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    LOG.warning(port)
    main(host='0.0.0.0', port=port)
