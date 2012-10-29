# import logging
# 
# from cStringIO import StringIO
# from tornado.httpclient import HTTPRequest
# from tornado.httpclient import HTTPResponse
# from unittest import TestCase
# 
# from bookie_parser.lib.readable import Readable
# 
# LOG = logging.getLogger()
# 
# 
# class TestReadableResponse(TestCase):
#     """Verify our response object works right."""
# 
#     def test_sample_request(self):
#         """Verify Readable takes a HTTPResponse"""
#         req = HTTPRequest('http://google.com')
#         mock = HTTPResponse(req, 200,
#                    buffer=StringIO("<html><head></head><body></body></html>"),
#                    headers={
#                     'Content-Encoding': 'gzip',
#                     'Transfer-Encoding': 'chunked',
#                     'Set-Cookie': 'CG=US:OH:Dayton; path=/',
#                     'Vary': 'Accept-Encoding, User-Agent',
#                     'Server': 'nginx',
#                     'Connection': 'keep-alive',
#                     'Cache-Control': 'max-age=60, private',
#                     'Date': 'Sat, 28 Apr 2012 19:35:08 GMT',
#                     'Content-Type': 'text/html'})
#         r = Readable(mock)
#         self.assertEqual(200, r.status_code)
#         self.assertFalse(r.is_error)
#         self.assertEqual('http://google.com', r.url)
#         self.assertEqual('text/html', r.content_type)
#         self.assertTrue(hasattr(r, 'headers'))
#         self.assertTrue(hasattr(r, 'content'))
#         self.assertTrue(r.content.startswith('<html>'))
#         self.assertTrue('OK', r.status_message)
#         self.assertEqual('google.com', r.domain)
#         self.assertEqual(None, r.request_time)
