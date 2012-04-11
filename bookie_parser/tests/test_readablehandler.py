import json
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
        test_url = urllib.quote_plus(
            'http://google.com/intl/en/about/index.html')
        LOG.error(test_url)
        LOG.error("/readable/" + test_url)
        response = self.fetch('/readable/' + test_url,
            method='GET',
            headers=headers)
        body = response.body
        resp = json.loads(body)

        self.assertIn("google.com", resp['readable'],
            'We should find google in the readable response. ' + body)
