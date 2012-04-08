"""Application main entry point for our tornado app"""
import os
import sys
import tornado.ioloop
import tornado.web

from tornado import template

# Template loader
TPL = template.Loader(os.path.join(os.path.dirname(__file__), 'tpl'))


from bookie_parser.logconfig import LOG
from bookie_parser.handlers import MainHandler
from bookie_parser.handlers import ReadableHandler


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/readable/(.*)", ReadableHandler),
])


def main(host='0.0.0.0', port=5000):
    LOG.info('starting server on port: ' + str(port))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    LOG.warning(port)
    main(host='0.0.0.0', port=port)
