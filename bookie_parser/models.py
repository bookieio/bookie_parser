import json
import logging
import os
import redis

from breadability.readable import Article
from bookie_parser.lib.readable import generate_hash

LOG = logging.getLogger(__name__)

redis_url = os.environ.get('OPENREDIS_URL', 'redis://localhost:6379')
server = redis.Redis.from_url(redis_url)


class WebPageMgr(object):
    """Manager for the WebPage data store object."""

    @staticmethod
    def exists(hash_id=None, url=None):
        if hash_id is None and url is not None:
            url = url.strip('/')
            hash_id = generate_hash(url)

        if server.exists(hash_id):
            return hash_id
        else:
            return None

    @staticmethod
    def get(hash_id=None):
        """"""
        if hash_id:
            if WebPageMgr.exists(hash_id=hash_id):
                doc = server.get(hash_id)
                js = json.loads(doc)
                # This might be a reference instead of a real doc of data.
                # If it is, load the hash_id the reference points to.
                if 'reference' in js:
                    doc = server.get(js['reference'])
                    js = json.loads(doc)
                return WebPage(**js)
        else:
            LOG.debug('Hash id not found: ' + str(hash_id))
            return None

    @staticmethod
    def store_request(read):
        """Store a readable document based off a ReadableRequest instance."""
        url = read.final_url
        hash_id = generate_hash(url)

        content = Article(read.content, url=url)
        readable_article = content.readable

        try:
            readable_title = content._original_document.title
        except AttributeError, exc:
            LOG.error(str(exc))
            readable_title = 'Unknown'

        # Json encoding a requests response breaks due to the CaseInsitiveDict
        # in use.
        request_info = {
            'content_type': read.content_type,
            'domain': read.domain,
            'final_url': read.final_url,
            'headers': dict(read.headers),
            'is_error': read.is_error,
            'request_time': read.request_time,
            'start_time': str(read.start_time),
            'status_code': read.status_code,
            'status_message': read.status_message,
            'url': read.url,
        }

        page = WebPage(
            hash_id=hash_id,
            readable=readable_article,
            request=request_info,
            title=readable_title,
            url=url,
        )

        server.set(hash_id, json.dumps(dict(page)))

        # If the url and the final url are not the same then store an extra
        # record pointing the original url to the final url record.
        if read.url != read.final_url:
            server.set(
                generate_hash(read.url),
                json.dumps({
                    'reference': hash_id
                })
            )

        return page


class WebPage(object):
    hash_id = None
    readable = None
    request = None
    title = None
    url = None

    def __init__(self, hash_id=None, url=None, readable=None,
                 title=None, request=None, final_url=None):
        """Create a new WebPage data instance."""
        if url:
            self.url = url
            if not hash_id:
                # Generate a new hash id
                self.hash_id = generate_hash(url)

        if hash_id:
            self.hash_id = hash_id
        if url:
            self.url = url
        if readable:
            self.readable = readable
        if request:
            self.request = request
        if self.request['is_error']:
            self.is_error = True
        if final_url:
            self.final_url = final_url

        if title:
            self.title = title

    def __iter__(self):
        keys = ['hash_id', 'readable', 'request', 'title', 'url']
        for key in keys:
            yield(key, getattr(self, key))
