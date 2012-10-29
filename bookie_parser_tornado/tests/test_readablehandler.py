# import json
# import logging
# import tornado
# import urllib
# 
# from tornado.testing import AsyncHTTPTestCase
# from tornado.testing import LogTrapTestCase
# 
# from bookie_parser import application
# 
# 
# LOG = logging.getLogger()
# 
# 
# class TestReadableHandler(AsyncHTTPTestCase, LogTrapTestCase):
#     def get_app(self):
#         return application
# 
#     def get_new_ioloop(self):
#         return tornado.ioloop.IOLoop.instance()
# 
#     def test_url_only(self):
#         """Verify we fetch/process a given url"""
#         headers = {'Accepts': 'application/json'}
#         test_url = urllib.quote_plus(
#             'http://google.com/intl/en/about/index.html')
#         LOG.error(test_url)
#         LOG.error("/readable/" + test_url)
#         response = self.fetch('/readable/' + test_url,
#             method='GET',
#             headers=headers)
#         body = response.body
#         resp = json.loads(body)
# 
#         self.assertIn("organize the world", resp['content'],
#             'We should find google in the readable response. ' + body)
# 
#     def test_response_keys(self):
#         """We expect to get a certain list of keys in our response"""
#         mandated_keys = [
#             'domain',
#             'url',
#             'is_error',
#             'content',
#             'content_type',
#             'headers',
#             'request_time',
#             'status_message',
#             'status_code',
#             'title',
#         ]
# 
#         headers = {'Accepts': 'application/json'}
#         test_url = urllib.quote_plus(
#             'http://google.com/intl/en/about/index.html')
#         response = self.fetch('/readable/' + test_url,
#             method='GET',
#             headers=headers)
#         data = json.loads(response.body)
#         for key in mandated_keys:
#             self.assertIn(key, data.keys())
