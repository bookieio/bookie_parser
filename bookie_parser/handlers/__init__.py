"""Tornado request handlers for our application."""
from tornado.web import RequestHandler

from bookie_parser import TPL
from bookie_parser.logconfig import LOG

class MainHandler(RequestHandler):
    """The main index handler."""
    def get(self):
        """Get '/' for main site page."""
        self.content_type = 'text/html'
        t = TPL.load('index.html')
        self.write(t.generate())


class ReadableHandler(RequestHandler):
    """Readable parsing routes."""

    def post(self, url):
        """Posting content will have it parsed and fed back to you in JSON."""
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
