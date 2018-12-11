import datetime
import enum
import uuid

from pyramid.config import Configurator
from pyramid.renderers import JSON
from pyramid.request import Request


def uuid_adapter(uuid_: uuid.UUID, _: Request):
    """
    Convert a `UUID` to it's hex string representation.

    :param uuid_: the UUID to convert.
    :param _: the request.
    """
    return uuid_.hex


def enum_adapter(enum_: enum.Enum, _: Request):
    """
    Convert an `Enum` into it's string value.

    :param enum_: the Enum object to convert.
    :param _: the request.
    """
    return enum_.value


def date_adapter(date_: datetime.date, _: Request):
    """
    Convert a date into a string representation as defined in ISO 8601.

    :param date_: the date object to convert.
    :param _: the request.
    """
    return date_.isoformat()


def datetime_adapter(datetime_: datetime.datetime, _: Request):
    """
    Convert a date into a string representation as defined in ISO 8601.

    :param datetime_: the date object to convert.
    :param _: the request.
    """
    return datetime_.replace(microsecond=0).isoformat()


def includeme(config: Configurator):
    """
    Setup the JSON renderer and attach the adapters for serialization.
    :param config: the config object.
    """
    json_renderer = JSON()
    json_renderer.add_adapter(uuid.UUID, uuid_adapter)
    json_renderer.add_adapter(enum.Enum, enum_adapter)
    json_renderer.add_adapter(datetime.date, date_adapter)
    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    config.add_renderer("json", json_renderer)
