import logging
import tornado
import urllib

from tornado.testing import AsyncHTTPTestCase
from tornado.testing import LogTrapTestCase
from tornado.web import RequestHandler
from tornado.web import Application

from bookie_parser import application
from bookie_parser.handlers import MainHandler


LOG = logging.getLogger()


class TestReadableHandler(AsyncHTTPTestCase, LogTrapTestCase):
    def get_app(self):
        return application

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()

    def test_url_only(self):
        """Verify we fetch/process a given url"""
        headers = {'Accepts': 'application/json'}
        test_url = urllib.quote_plus('http://google.com/intl/en/about/index.html')
        LOG.error(test_url)
        LOG.error("/view/" + test_url)
        response = self.fetch('/view/' + test_url,
            method='GET',
            headers=headers)
        body = response.body
        self.assertIn("google.com", body,
            'We should find google in the body. ' + body)
