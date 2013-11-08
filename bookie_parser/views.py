import json
import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import render_to_response
from pyramid.view import view_config

from bookie_parser.lib.readable import ReadableRequest
from bookie_parser.models import WebPageMgr
# @TODO HTTPFound redirect the /readable /r to the api/v1/xxx


LOG = logging.getLogger(__name__)


@view_config(route_name='index', renderer='index.mako')
def index(request):
    return {}


@view_config(route_name='api_hash', renderer='json')
def api_hash(request):
    """Fetch the data based on the given hash id."""
    # Look up the data from the hash_id
    hash_id = request.matchdict.get('hash_id', None)
    if not hash_id:
        LOG.debug('no hash id supplied: ' + hash_id)
        return HTTPNotFound()

    exists = WebPageMgr.exists(hash_id=hash_id)
    if not exists:
        request.response.status_int = 404
        return {
            'error': 'Hash id not found: ' + hash_id,
        }

    page = WebPageMgr.get(exists)
    if not page:
        LOG.debug('notfound: ' + hash_id)
        return HTTPNotFound()

    resp = request.response
    environ = request.environ
    resp.headers['Content-Type'] = 'application/json'
    # allow cross domain requests: xdr
    resp.headers['Access-Control-Allow-Origin'] = environ.get('HTTP_ORIGIN',
            "")

    return {
        'data': dict(page),
        'readable': page.readable,
    }


@view_config(route_name='api_parser_options')
def api_parser_options(request):
    resp = request.response
    environ = request.environ
    resp.headers = {}
    resp.headers['Access-Control-Allow-Origin'] = environ['HTTP_ORIGIN']
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    resp.headers['Access-Control-Max-Age'] = '1000'
    resp.headers['Access-Control-Allow-Headers'] = (
        '*'
        ',x-requested-with,Content-Type')
    return request.response


@view_config(route_name='api_parser', renderer='json')
def api_parse(request):
    """Api to parse a url POST'd"""
    url = request.params.get('url', None)

    resp = request.response
    environ = request.environ
    resp.headers['Access-Control-Allow-Origin'] = environ.get(
        'HTTP_ORIGIN', '')

    if not url:
        params = request.json_body
        LOG.debug(params)
        url = params.get('url', None)

        if not url:
            request.response.status_int = 404
            return {
                'error': 'No url supplied.',
            }

    LOG.debug('api process, ' + url)

    url = url.strip('/')
    LOG.debug('Checking url: ' + url)
    exists = WebPageMgr.exists(url=url)
    if exists:
        LOG.debug('Exists: ...forwarding')
        request.matchdict['hash_id'] = exists
        return api_hash(request)
    else:
        LOG.debug('Does not Exist: ...fetching')
        read = ReadableRequest(url)
        read.process()

        if not read.is_error:
            page = WebPageMgr.store_request(read)
            request.matchdict['hash_id'] = page.hash_id
            return api_hash(request)
        else:
            LOG.error('url_is_error,' + url)
            request.response.status_int = 500
            return {
                'error': 'There was an error fetching content.',
            }


@view_config(route_name='readable_short', renderer="json")
@view_config(route_name='readable', renderer="json")
def readable(request):
    """This is the old api endpoint that returns json data.

    """
    url = request.params.get('url', None)
    LOG.debug('readable process, ' + url)

    if not url:
        LOG.debug('notfound,' + url)
        return HTTPNotFound()

    url = url.strip('/')
    LOG.debug('Checking url: ' + url)

    request.response.headers['Content-Type'] = 'application/json'
    # allow cross domain requests: xdr
    request.response.headers['Access-Control-Allow-Origin'] = '*'

    exists = WebPageMgr.exists(url=url)
    if exists:
        page = WebPageMgr.get(exists)
        return {
            'data': dict(page),
            'readable': page.readable,
        }
    else:
        LOG.debug('Does not Exist: ...fetching')
        read = ReadableRequest(url)
        read.process()

        if not read.is_error:
            page = WebPageMgr.store_request(read)

            return {
                'data': dict(page),
                'readable': page.readable
            }
        else:
            LOG.error('url_is_error,' + url)
            request.response.status_int = 500
            error_message = 'There was an error reading the page.'
            return {
                'error': error_message
            }


@view_config(route_name='view_short')
@view_config(route_name='view')
def view(request):
    """This is the 'usable' endpoint that displays the trimmed content for
    reading.

    """
    # fetch download of the url
    url = request.params.get('url', None)
    LOG.debug('process, ' + url)

    if not url:
        LOG.debug('notfound,' + url)
        return HTTPNotFound()

    url = url.strip('/')
    LOG.debug('Checking url: ' + url)

    exists = WebPageMgr.exists(url=url)
    if exists:
        LOG.debug('Exists: ...forwarding')
        return HTTPFound(
            location=request.route_url('url', hash_id=exists))

    else:
        LOG.debug('Does not Exist: ...fetching')
        read = ReadableRequest(url)
        read.process()

        if not read.is_error:
            LOG.warning('writing it out')
            page = WebPageMgr.store_request(read)
            return HTTPFound(
                location=request.route_url('url', hash_id=page.hash_id))
        else:
            LOG.error('url_is_error,' + url)
            return render_to_response(
                'error.mako', {
                    'error_message': 'There was an error fetching the url.',
                    'error_details': {
                        'code': read.status_code,
                    },
                    'readable': read,
                    'title': 'Processing Error',
                },
                request=request
            )


@view_config(route_name='url', renderer='readable.mako')
def url(request):
    """"""
    # Look up the url from the hash_id
    hash_id = request.matchdict.get('hash_id', None)
    page = WebPageMgr.get(hash_id)

    if page:
        return {
            'webpage': page,
        }
    else:
        return HTTPNotFound()


@view_config(route_name='redis_list', renderer='redis_list.mako')
def redis_list(request):
    """List out the items in redis."""
    from bookie_parser.models import server
    urls = {}
    refs = []

    for hash_id in server.keys('*'):
        data = json.loads(server.get(hash_id))
        if 'reference' in data:
            refs.append(data['reference'])
        else:
            urls[data['hash_id']] = data

    return {
        'urls': urls,
        'refs': refs,
    }
