from pyramid.config import Configurator


def includeme(config: Configurator):
    ###
    # USER
    ###

    config.add_route(
        name="current_user.settings",
        path="/settings",
        request_method="POST"
    )

    config.add_route(
        name="current_user.extend",
        path="/extend",
        request_method="POST"
    )
