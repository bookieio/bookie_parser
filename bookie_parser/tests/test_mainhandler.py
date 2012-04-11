import logging

from tornado.testing import AsyncHTTPTestCase
from tornado.testing import LogTrapTestCase
from tornado.web import RequestHandler
from tornado.web import Application

from bookie_parser import application
from bookie_parser.handlers import MainHandler


LOG = logging.getLogger()


class TestMainHandler(AsyncHTTPTestCase, LogTrapTestCase):
    def get_app(self):
        return application

    def test_index(self):
        """Check the index loads template properly."""
        response = self.fetch("/")
        body = response.body
        self.assertIn('Bookie', body, 'Must find Bookie in our body: ' + body)
