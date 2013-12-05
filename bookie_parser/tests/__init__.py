from pyramid import testing
import redis
from webtest import TestApp

import bookie_parser.models

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class WebTestBase(unittest.TestCase):

    def setUp(self):
        redis_url = 'redis://localhost:6379/9'
        bookie_parser.models.server = redis.Redis.from_url(redis_url)
        bookie_parser.models.server.flushdb()

        from bookie_parser import main
        app = main({}, google_analytics='123')
        self.app = TestApp(app)

    def tearDown(self):
        testing.tearDown()
        self.app = None
        # Make sure to wipe our data store after each run.
        bookie_parser.models.server.flushdb()
