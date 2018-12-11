import datetime
from math import radians, sin, atan2, sqrt, cos

import googlemaps
from pyramid.httpexceptions import HTTPNoContent
from pyramid.request import Request
from pyramid.view import view_defaults, view_config

from hackathon_la.client import GoogleClient
from hackathon_la.core.container.core import Database, Core
from hackathon_la.repository import CarRepository


@view_defaults(renderer="json")
class CarDetailsAPI:
    THRESHOLD = 900  # 15 minutes

    def __init__(self, request: Request):
        self._request = request
        self._google_client = GoogleClient(
            google_client=googlemaps.Client(key=Core.config.google_api_key())
        )
        self._car_repository = CarRepository(Database.session())

    @view_config(route_name='current_user.notification', request_method='GET')
    def get_notification_data_handler(self):
        user_latitude = float(self._request.params.get("lat"))
        user_longitude = float(self._request.params.get("lon"))
        user_location = (user_latitude, user_longitude)

        address, distance, duration, end_date = self._calculate_matrix(user_location)
        if datetime.datetime.utcnow() + datetime.timedelta(seconds=duration + self.THRESHOLD) >= end_date:
            return {
                "notification_type": "MUST_GO",
                "time_required": duration,
                "distance": distance,
                "address": address
            }

        return HTTPNoContent()

    def _calculate_matrix(self, user_location):
        """
        calculates the user's distance, duration and gets the address and the
        booking's end date
        :param user_location: the user's location tuple coordinates
        :return:
        """
        car = self._car_repository.get_car()
        car_location = (car.lat, car.lon)
        park_location = (car.parking_spot_lat, car.parking_spot_lon)
        user_car_distance = _calculate_distance(user_location, car_location)
        user_car_matrix = None
        if user_car_distance > 50:
            user_car_matrix = self._google_client \
                .get_matrix_response(user_location, car_location,
                                     mode="walking")
        car_park_matrix = self._google_client \
            .get_matrix_response(user_location, park_location)

        address = car_park_matrix.address
        if user_car_matrix:
            duration = user_car_matrix.duration + car_park_matrix.duration
            distance = user_car_matrix.distance + car_park_matrix.distance
        else:
            duration = car_park_matrix.duration
            distance = car_park_matrix.distance
        return address, distance, duration, car.booking[0].end_date


def _calculate_distance(origin: tuple, destination: tuple) -> int:
    R = 6373.0

    lat1 = radians(origin[0])
    lon1 = radians(origin[1])
    lat2 = radians(destination[0])
    lon2 = radians(destination[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return int(R * c * 1000)
