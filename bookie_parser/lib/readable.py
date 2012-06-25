"""Readable is response we're passing back based on our work here.

We need to provide back to the caller

- url
- is_error
- content
- content_type
- headers (response)
- status_message (Ok)
- status_code (200)
- domain
- request_time

"""
from httpcode import STATUS_CODES
from urlparse import urlparse


class Readable(object):
    """Readable response object."""
    status_code = None
    content = ""
    content_type = ""
    headers = {}
    url = ""

    def __init__(self, response):
        """Process a response object to build our Readable

        :param response: HTTPResponse

        """
        self.status_code = response.code
        self.content = response.body
        self.content_type = response.headers.get('Content-Type', None)
        self.headers = response.headers
        self.request_time = response.request_time
        self.url = response.request.url

    @property
    def domain(self):
        """What is the root domain of the request we did."""
        return urlparse(self.url).netloc

    @property
    def is_error(self):
        """Verify our status code is an error/not."""
        # simple first check, if it's not a 2xx, then it's an error
        return False if str(self.status_code).startswith('2') else False

    @property
    def status_message(self):
        """Fetch the status message from the httpcode library."""
        # This is a tuple of short message, long message. We only care for the
        # short version.
        return STATUS_CODES[self.status_code][0]
