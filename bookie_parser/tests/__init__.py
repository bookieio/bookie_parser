import fakeredis
import unittest
from pyramid import testing
from webtest import TestApp

import bookie_parser.models


class WebTestBase(unittest.TestCase):

    def setUp(self):
        # Set up the fake redis server instance.
        bookie_parser.models.server = fakeredis.FakeRedis()
        from bookie_parser import main
        app = main({}, google_analytics='123')
        self.app = TestApp(app)

    def tearDown(self):
        testing.tearDown()
        self.app = None
        # Make sure to wipe our data store after each run.
        bookie_parser.models.server.flushdb()
