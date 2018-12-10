import transaction
from dependency_injector import containers, providers
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from hackathon_la.model import get_tm_session, get_session_factory


class Core(containers.DeclarativeContainer):
    config = providers.Configuration('config')


class Database(containers.DeclarativeContainer):
    session = providers.ThreadLocalSingleton(
        get_tm_session,
        providers.Singleton(
            get_session_factory,
            engine=providers.Factory(
                engine_from_config,
                Core.config,
                prefix='sqlalchemy_')),
        transaction
    )


def setup_containers(settings):
    """
    This method converts all the dots in settings into underscores and updates
    the Core configurator with these settings.
    :param settings: a dictionary with application settings.
    """
    settings_ = {}
    for key, value in settings.items():
        key_ = key.replace('.', '_')
        settings_[key_] = value
    Core.config.update(settings_)


def includeme(config: Configurator):
    """
    Setup the Core configurator, from here the database session and everything
    else can be constructed.
    :param config: the `Configurator` object passed by the Pyramid framework.
    """
    settings = config.get_settings()
    setup_containers(settings)
