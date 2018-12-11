import datetime
from math import radians, sin, atan2, sqrt, cos
from time import sleep

import dateutil.parser
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

    @view_config(route_name='current_user.settings', request_method='POST')
    def get_notification_data_handler(self):
        data = self._request.json_body

        self._google_client.get_nearest_gas_station((37.31917, -122.04511))

        user_pos = (float(data["user"]["x"]), float(data["user"]["y"]))
        car_pos = (float(data["car"]["x"]), float(data["car"]["y"]))
        fuel = int(data["car"]["fuel"])
        parking_pos = (float(data["parking"]["x"]), float(data["parking"]["y"]))
        end_date = dateutil.parser.parse(data["booking"]["expires"], ignoretz=True)

        address, distance, duration = self._calculate_matrix(user_pos, car_pos, parking_pos)

        # check if user needs to refuel
        gs_pos = None
        if fuel < 25:
            gas_station_pos_dict = self._google_client.get_nearest_gas_station(car_pos)
            gs_pos = (gas_station_pos_dict["lat"], gas_station_pos_dict["lng"])
            gs_address, gs_distance, gs_duration = self._calculate_matrix(car_pos, car_pos, gs_pos)
            distance = distance + gs_distance
            duration = duration + gs_duration

        if datetime.datetime.utcnow() + datetime.timedelta(seconds=duration + self.THRESHOLD) >= end_date:
            res = {
                "data": {
                    "time_required": duration,
                    "distance": distance,
                    "address": address
                },
                "request": data
            }
            if gs_pos:
                res["gas_station"] = {
                    "lat": f"{gs_pos[0]}",
                    "lon": f"{gs_pos[1]}"
                }
            return res
        return {"request": data}

    @view_config(route_name='current_user.extend', request_method='POST')
    def extend_date_handler(self):
        data = self._request.json_body
        car = self._car_repository.get_car()

        booking = car.booking[0]
        booking.end_date = booking.end_date + datetime.timedelta(
            seconds=int(data["seconds"]))
        self._car_repository.save(booking)

        sleep(1)
        return HTTPNoContent()

    def _calculate_matrix(self, user_pos, car_pos, parking_pos):
        """
        calculates the user's distance, duration and gets the address and the
        booking's end date
        :param user_pos: the user's location tuple coordinates
        :return:
        """
        user_car_distance = _calculate_distance(user_pos, car_pos)
        user_car_matrix = None
        if user_car_distance > 50:
            user_car_matrix = self._google_client \
                .get_matrix_response(user_pos, car_pos,
                                     mode="walking")
        car_park_matrix = self._google_client \
            .get_matrix_response(user_pos, parking_pos)

        address = car_park_matrix.address
        if user_car_matrix:
            duration = user_car_matrix.duration + car_park_matrix.duration
            distance = user_car_matrix.distance + car_park_matrix.distance
        else:
            duration = car_park_matrix.duration
            distance = car_park_matrix.distance
        return address, distance, duration


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
