"""Tornado request handlers for our application."""
from tornado import httpclient
from tornado.web import asynchronous
from tornado.web import HTTPError
from tornado.web import RequestHandler
from readability_lxml.readability import Document

from bookie_parser.lib.readable import Readable
from bookie_parser.logconfig import LOG


MAX_REDIRECTS = 10
MAX_REDIRECT_ERROR = 599


class MainHandler(RequestHandler):
    """The main index handler."""
    def get(self):
        """Get '/' for main site page."""
        self.content_type = 'text/html'
        self.render('index.html')


def _fetch_url(url, callback):
    """Shared helper to fetch the url requested to be readable"""
    httpclient.AsyncHTTPClient.configure(
        "tornado.curl_httpclient.CurlAsyncHTTPClient")
    http = httpclient.AsyncHTTPClient()
    try:
        http.fetch(url, callback, max_redirects=MAX_REDIRECTS)
    except httpclient.HTTPError, exc:
        LOG.error(exc)


def _process_fetch_url(response, callback):
    """Process the fetched url which returns a Readable object"""
    if response.code == 599:
        LOG.error(response.error.code)
        LOG.error(response.error.message)()
        LOG.error(response.error.response)
        raise response.error
    else:
        readable = Readable(response)
        callback(readable)


class ReadableHandler(RequestHandler):
    """Readable parsing routes."""

    @asynchronous
    def get(self, url):
        """Getting will fetch the content for the url."""
        _fetch_url(url, self._on_download)

    def _on_download(self, response):
        """On downloading the url content, make sure we readable it."""
        _process_fetch_url(response, self._readable_content)

    def _readable_content(self, readable_response):
        """Shared helper to process and respond with the content."""
        self.content_type = 'application/json'
        self.add_header('Access-Control-Allow-Origin', '*')

        doc = Document(readable_response.content,
                url=readable_response.url)
        readable_article = doc.summary(enclose_with_html_tag=False)

        try:
            readable_title = doc.title()
        except AttributeError, exc:
            LOG.error(str(exc))
            readable_title = 'Unknown'
        resp = {
            'url': readable_response.url,
            'content_type': readable_response.content_type,
            'domain': readable_response.domain,
            'headers': readable_response.headers,
            'is_error': readable_response.is_error,
            'content': readable_article,
            'short_title': doc.short_title(),
            'status_code': readable_response.status_code,
            'status_message': readable_response.status_message,
            'title': readable_title,
            'request_time': readable_response.request_time,
        }
        self.write(resp)
        self.finish()

    def post(self, url):
        """Posting content will have it parsed and fed back to you in JSON."""
        content = self.get_argument('content')
        self._readable_content(url, content)


class ViewableHandler(RequestHandler):
    """I want to be readable parsed, but returned for viewing."""

    @asynchronous
    def get(self, url):
        """Getting will fetch the content for the url."""
        _fetch_url(url, self._on_download)

    @asynchronous
    def post(self):
        """Getting will fetch the content for the url."""
        url = self.get_argument('url')
        LOG.error(url)

        if not url:
            raise HTTPError(404)

        _fetch_url(url, self._on_download)

    def _on_download(self, response):
        """On downloading the url content, make sure we readable it."""
        _process_fetch_url(response, self._readable_content)

    def _readable_content(self, readable):
        """Shared helper to process and respond with the content."""
        self.content_type = 'text/html'

        doc = Document(readable.content, url=readable.url)
        readable_article = doc.summary(enclose_with_html_tag=False)
        try:
            readable_title = doc.title()
        except AttributeError, exc:
            LOG.error(str(exc))
            readable_title = 'Unknown'

        self.render('readable.html',
            readable=readable,
            content=readable_article,
            short_title=doc.short_title(),
            title=readable_title,
        )
