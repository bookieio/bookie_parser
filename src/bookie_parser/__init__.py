"""Application main entry point for our tornado app"""
import logging
import os
import sys
import time
import tornado.ioloop
import tornado.web
import urllib

from collections import namedtuple
from readability.readability import Document

# For pretty log messages, if available
try:
    import curses
except ImportError:
    curses = None

# Logging bits stolen and adapted from:
# http://www.tornadoweb.org/documentation/_modules/tornado/options.html
LOGLEVEL="DEBUG"
LogOptions = namedtuple('LogOptions', [
    'loglevel',
    'log_file_prefix',
    'log_file_max_size',
    'log_file_num_backups',
    'log_to_stderr',
])

options = LogOptions(
    loglevel=LOGLEVEL,
    log_file_prefix="",
    log_file_max_size=100 * 1000 * 1000,
    log_file_num_backups=5,
    log_to_stderr=True,
)

def enable_pretty_logging():
    """Turns on formatted logging output as configured.

    This is called automatically by `parse_command_line`.
    """
    root_logger = logging.getLogger()
    if options.log_file_prefix:
        channel = logging.handlers.RotatingFileHandler(
            filename=options.log_file_prefix,
            maxBytes=options.log_file_max_size,
            backupCount=options.log_file_num_backups)
        channel.setFormatter(_LogFormatter(color=False))
        root_logger.addHandler(channel)

    if (options.log_to_stderr or
        (options.log_to_stderr is None and not root_logger.handlers)):
        # Set up color if we are in a tty and curses is installed
        color = False
        if curses and sys.stderr.isatty():
            try:
                curses.setupterm()
                if curses.tigetnum("colors") > 0:
                    color = True
            except Exception:
                pass
        channel = logging.StreamHandler()
        channel.setFormatter(_LogFormatter(color=color))
        root_logger.addHandler(channel)


class _LogFormatter(logging.Formatter):
    def __init__(self, color, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)
        self._color = color
        if color:
            # The curses module has some str/bytes confusion in python3.
            # Most methods return bytes, but only accept strings.
            # The explict calls to unicode() below are harmless in python2,
            # but will do the right conversion in python3.
            fg_color = unicode(curses.tigetstr("setaf") or
                               curses.tigetstr("setf") or "", "ascii")
            self._colors = {
                logging.DEBUG: unicode(curses.tparm(fg_color, 4), # Blue
                                       "ascii"),
                logging.INFO: unicode(curses.tparm(fg_color, 2), # Green
                                      "ascii"),
                logging.WARNING: unicode(curses.tparm(fg_color, 3), # Yellow
                                         "ascii"),
                logging.ERROR: unicode(curses.tparm(fg_color, 1), # Red
                                       "ascii"),
            }
            self._normal = unicode(curses.tigetstr("sgr0"), "ascii")

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception, e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)
        record.asctime = time.strftime(
            "%y%m%d %H:%M:%S", self.converter(record.created))
        prefix = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]' % \
            record.__dict__
        if self._color:
            prefix = (self._colors.get(record.levelno, self._normal) +
                      prefix + self._normal)
        formatted = prefix + " " + record.message
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted = formatted.rstrip() + "\n" + record.exc_text
        return formatted.replace("\n", "\n    ")


# Set up log level and pretty console logging by default
logging.getLogger().setLevel(getattr(logging, LOGLEVEL))
enable_pretty_logging()
LOG = logging.getLogger()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class ReadableHandler(tornado.web.RequestHandler):
    def post(self, url):
        content = self.get_argument('content')

        # html = urllib.urlopen(url).read()
        doc = Document(content)
        readable_article = doc.summary()
        try:
            readable_title = doc.short_title()
        except AttributeError, exc:
            LOG.error(str(exc))
            readable_title = 'Unknown'
        resp = {
            'url': url,
            'readable': readable_article,
            'title': readable_title,
        }
        self.content_type = 'application/json'
        self.write(resp)


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/readable/(.*)", ReadableHandler),
])


def main(port=5000):
    LOG.info('starting server on port: ' + str(port))
    port = int(os.environ.get("PORT", port))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

