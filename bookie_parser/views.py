import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
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

    request.response.headers['Content-Type'] = 'application/json'
    # allow cross domain requests: xdr
    request.response.headers['Access-Control-Allow-Origin'] = request.environ['HTTP_ORIGIN']

    return {
        'data': dict(page),
        'readable': page.readable,
    }


@view_config(route_name='api_parser_options')
def api_parser_options(request):
      request.response.headers = {}
      request.response.headers['Access-Control-Allow-Origin'] = request.environ['HTTP_ORIGIN']
      request.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
      request.response.headers['Access-Control-Max-Age'] = '1000'
      request.response.headers['Access-Control-Allow-Headers'] = '*,x-requested-with,Content-Type'
      return request.response


@view_config(route_name='api_parser', renderer='json')
def api_parse(request):
    """Api to parse a url POST'd"""
    url = request.params.get('url', None)
    request.response.headers['Access-Control-Allow-Origin'] = request.environ['HTTP_ORIGIN']

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
            readable_article = 'There was an error.'

            return {
                'data': page,
                'readable': readable_article,
            }


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
