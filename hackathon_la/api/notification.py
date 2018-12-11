import logging

import googlemaps
from pyramid.request import Request
from pyramid.view import view_defaults, view_config

from hackathon_la.core.container.core import Database
from hackathon_la.repository import CarRepository


@view_defaults(renderer="json")
class CarDetailsAPI:
    _LOG = logging.getLogger(__name__)

    def __init__(self, request: Request):
        self._request = request
        self._gmaps = googlemaps.Client(
            key="API_KEY")
        self._car_repository = CarRepository(Database.session())

    @view_config(route_name='current_user.notification', request_method='GET')
    def get_notification_data_handler(self):
        user_latitude = self._request.params.get("lat")
        user_longitude = self._request.params.get("lon")
        origin = (user_latitude, user_longitude)

        car = self._car_repository.get_car()
        destination = (car.parking_spot_lat, car.parking_spot_lon)

        res = self._gmaps.distance_matrix(origin, destination)

        distance_value = res["rows"][0]["elements"][0]["distance"]["value"]
        duration_value = res["rows"][0]["elements"][0]["duration"]["value"]
        destination_address = res["destination_addresses"][0]

        return {
            "notification_type": "MUST_GO",
            "time_required": duration_value,
            "distance": distance_value,
            "address": destination_address
        }
