from pyramid.config import Configurator
from pyramid.events import NewRequest


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):

        response.headers.update({
            'Access-Control-Allow-Origin': "*"
        })

        if request.method == 'OPTIONS':
            response.headers.update({
                'Access-Control-Allow-Methods':
                    'POST, GET, DELETE, PUT, OPTIONS',
                'Access-Control-Allow-Headers':
                    'Origin, Content-Type, X-Requested-With, Authorization',
                'Access-Control-Max-Age': '86400'
            })
            response.status_code = 200
            return response

    event.request.add_response_callback(cors_headers)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    config.include("hackathon_la.core.container.core")
    config.include("hackathon_la.core.renderer")
    config.include("hackathon_la.model")
    config.include("hackathon_la.routes")
    config.scan()
    return config.make_wsgi_app()
