from pyramid.config import Configurator


def includeme(config: Configurator):
    ###
    # USER
    ###

    config.add_route(
        name="current_user.notification",
        path="/notification",
        request_method="GET"
    )
