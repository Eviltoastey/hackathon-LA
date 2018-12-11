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

    config.add_route(
        name="current_user.dashboard",
        path="/dashboard",
        request_method="GET"
    )

    config.add_route(
        name="current_user.extend",
        path="/extend",
        request_method="POST"
    )
