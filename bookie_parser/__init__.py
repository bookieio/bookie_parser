from pyramid.config import Configurator


MAX_REDIRECTS = 10
MAX_REDIRECT_ERROR = 599


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Make sure we setup a directory for the templates to come out of.
    settings['mako.directories'] = 'bookie_parser:templates'

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')

    config.add_route('readable_short', '/r')
    config.add_route('readable', '/readable')
    config.add_route('view_short', '/v')
    config.add_route('view', '/view')
    config.add_route('url', '/u/{hash_id}')

    # Start an api end point we should be using that allows us options to
    # gather extra data.
    config.add_route('api_parser_options',
        '/api/v1/parse',
        request_method="OPTIONS")
    config.add_route('api_parser', '/api/v1/parse', request_method="POST")
    config.add_route('api_hash', '/api/v1/{hash_id}')

    config.scan()
    return config.make_wsgi_app()
