# import logging
# from bookie_parser.tests import WebTestBase
# 
# LOG = logging.getLogger()
# 
# 
# class TestIndex(WebTestBase):
# 
#     def test_index(self):
#         """Check the index loads template properly."""
#         response = self.app.get("/")
#         body = response.body
#         self.assertIn(
#             'Bookie', body,
#             'Must find Bookie in our body: ' + body)
