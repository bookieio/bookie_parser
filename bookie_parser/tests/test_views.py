import json
import logging

from bookie_parser.lib.readable import generate_hash
from bookie_parser.models import WebPageMgr
from bookie_parser.tests import WebTestBase


LOG = logging.getLogger()


class TestViewable(WebTestBase):

    def test_viewable_response(self):
        """Make sure we can load and get a html response correctly."""
        url = 'http://www.google.com/intl/en/about/index.html'
        hashed = generate_hash(url)
        resp = self.app.get(
            '/v',
            params={
                'url': url
            },
            status=302)

        # follow the redirect and we land at the actual page.
        resp = resp.follow()
        body = resp.body

        self.assertTrue(
            resp.request.url.endswith(hashed),
            'the url should end with the url hash')
        self.assertIn(
            "google.com", body,
            'we should find google in the body. ' + body)

    def test_missing_viewable_response(self):
        """A missing hash id will return a 404."""
        resp = self.app.get('/u/123notthere', status=404)
        self.assertEqual(
            404,
            resp.status_code,
            'Returns a 404 for the missing hash id.')

    def test_cached_webpage(self):
        """When we readable parse we cache the data in redis."""
        url = 'http://www.google.com/intl/en/about/index.html'
        hashed = generate_hash(url)
        resp = self.app.get(
            '/v',
            params={
                'url': url
            },
            status=302)

        # follow the redirect and we land at the actual page.
        resp = resp.follow()

        from bookie_parser.models import server
        # Make sure the data exists in redis
        self.assertTrue(server.get(hashed), 'The key is found.')

        # Now hit up our redis server and find what data we've stored.
        data = WebPageMgr.get(hash_id=hashed)

        self.assertEqual(
            url, data.url,
            "The url is stored in the root object")
        self.assertEqual(
            hashed, data.hash_id,
            "The hash is stored in the root object")
        self.assertTrue(
            data.request is not None,
            'The request is stored in the cache.')
        self.assertEqual(
            u'Google  - About Google',
            data.title)
        self.assertTrue(data.readable is not None)


class TestReadableJSON(WebTestBase):
    """Testing the legacy and should go away JSON 'api'-like view.

    This is going to be deprecated in factor of the real api, but wtf, let's
    keep it around for one more iteration.

    """

    def test_readable_response(self):
        """Make sure we can load and get a json response correctly."""
        url = 'http://www.google.com/intl/en/about/index.html'
        resp = self.app.get(
            '/r',
            params={
                'url': url
            },
            status=200)

        # follow the redirect and we land at the actual page.
        body = json.loads(resp.body)

        self.assertTrue('data' in body)
        self.assertTrue('readable' in body)

    def test_readable_error(self):
        """Now break it and get a 500."""
        url = 'http://123456789018234.com'
        resp = self.app.get(
            '/r',
            params={
                'url': url
            },
            status=500)

        # Load the page and we should get a nice error.
        body = json.loads(resp.body)
        self.assertTrue('error' in body)


class TestApi(WebTestBase):
    """Let's have a real API we test against.

    """

    def test_api_call(self):
        """Calling the parse api with a url gets you all the data."""
        url = 'http://www.google.com/intl/en/about/index.html'
        hashed = generate_hash(url)
        resp = self.app.post(
            '/api/v1/parse',
            params={
                'url': url
            },
            extra_environ={
                'HTTP_ORIGIN': '127.0.0.1'
            },
            status=200)

        # follow the redirect and we land at the actual page.
        body = json.loads(resp.body)
        self.assertIn('data', body)
        self.assertIn('readable', body)
