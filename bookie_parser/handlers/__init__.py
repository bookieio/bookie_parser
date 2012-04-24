"""Tornado request handlers for our application."""
from tornado import httpclient
from tornado.web import asynchronous
from tornado.web import HTTPError
from tornado.web import RequestHandler
from readability_lxml.readability import Document
from urlparse import urlparse

from bookie_parser.logconfig import LOG


MAX_REDIRECTS = 10
MAX_REDIRECT_ERROR = 599


class MainHandler(RequestHandler):
    """The main index handler."""
    def get(self):
        """Get '/' for main site page."""
        self.content_type = 'text/html'
        self.render('index.html')


class ReadableHandler(RequestHandler):
    """Readable parsing routes."""

    @asynchronous
    def get(self, url):
        """Getting will fetch the content for the url."""
        httpclient.AsyncHTTPClient.configure(
            "tornado.curl_httpclient.CurlAsyncHTTPClient")
        http = httpclient.AsyncHTTPClient()
        try:
            http.fetch(url, self._on_download, max_redirects=MAX_REDIRECTS)
        except httpclient.HTTPError, exc:
            LOG.error(e)

    def _on_download(self, response):
        """On downloading the url content, make sure we readable it."""
        LOG.info(response.request_time)

        if response.code == MAX_REDIRECT_ERROR:
            raise('MAX REDIRECTS HIT')
        else:
            self._readable_content(response.request.url, response.body)

        self.finish()

    def _readable_content(self, url, content):
        """Shared helper to process and respond with the content."""
        self.content_type = 'application/json'

        doc = Document(content, url=url)
        readable_article = doc.summary(enclose_with_html_tag=False)

        try:
            readable_title = doc.title()
        except AttributeError, exc:
            LOG.error(str(exc))
            readable_title = 'Unknown'
        resp = {
            'url': url,
            'domain': urlparse(url).netloc,
            'readable': readable_article,
            'short_title': doc.short_title(),
            'title': readable_title,
        }
        self.write(resp)

    def post(self, url):
        """Posting content will have it parsed and fed back to you in JSON."""
        content = self.get_argument('content')
        self._readable_content(url, content)


class ViewableHandler(RequestHandler):
    """I want to be readable parsed, but returned for viewing."""

    @asynchronous
    def get(self, url):
        """Getting will fetch the content for the url."""
        httpclient.AsyncHTTPClient.configure(
            "tornado.curl_httpclient.CurlAsyncHTTPClient")
        http = httpclient.AsyncHTTPClient()
        try:
            http.fetch(url, self._on_download, max_redirects=MAX_REDIRECTS)
        except httpclient.HTTPError, exc:
            LOG.error(e)

    @asynchronous
    def post(self):
        """Getting will fetch the content for the url."""
        httpclient.AsyncHTTPClient.configure(
            "tornado.curl_httpclient.CurlAsyncHTTPClient")
        http = httpclient.AsyncHTTPClient()
        url = self.get_argument('url')
        LOG.error(url)

        if not url:
            raise HTTPError(404)

        try:
            http.fetch(url, self._on_download, max_redirects=MAX_REDIRECTS)
        except httpclient.HTTPError, exc:
            LOG.error(e)


    def _on_download(self, response):
        """On downloading the url content, make sure we readable it."""
        LOG.info(response)
        LOG.info(response.request_time)
        LOG.info(response.body)
        LOG.info(response.request.url)

        if response.code == 599:
            LOG.error(response.error.code)
            LOG.error(response.error.message)()
            LOG.error(response.error.response)
            raise response.error
        else:
            self._readable_content(response.request.url, response.body)

    def _readable_content(self, url, content):
        """Shared helper to process and respond with the content."""
        self.content_type = 'text/html'

        LOG.info(type(content))
        doc = Document(content, url=url)
        readable_article = doc.summary(enclose_with_html_tag=False)
        try:
            readable_title = doc.title()
        except AttributeError, exc:
            LOG.error(str(exc))
            readable_title = 'Unknown'

        self.render('readable.html',
            content=readable_article,
            domain=urlparse(url).netloc,
            short_title=doc.short_title(),
            title=readable_title,
            url=url)
