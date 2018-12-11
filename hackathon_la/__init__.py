from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include("hackathon_la.core.container.core")
    config.include("hackathon_la.model")
    config.include("hackathon_la.routes")
    config.scan()
    return config.make_wsgi_app()
