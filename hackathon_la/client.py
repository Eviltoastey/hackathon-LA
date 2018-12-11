from __future__ import annotations

from dataclasses import dataclass

from googlemaps import Client
from pyramid.httpexceptions import HTTPBadRequest


class GoogleClient:
    def __init__(self, google_client: Client) -> None:
        self._google_client = google_client

    def get_matrix_response(self, origin, destination, mode="driving") -> MatrixResponse:
        res = self._google_client.distance_matrix(origin, destination, mode)

        try:
            distance_value = res["rows"][0]["elements"][0]["distance"]["value"]
            duration_value = res["rows"][0]["elements"][0]["duration"]["value"]
        except Exception:
            raise HTTPBadRequest("GOOGLE SUCKS")
        destination_address = res["destination_addresses"][0]

        return MatrixResponse(
            distance=distance_value,
            duration=duration_value,
            address=destination_address
        )

    def get_nearest_gas_station(self, car_pos):
        location_bias = f"circle:{10000}@{car_pos[0]},{car_pos[1]}"
        return self._google_client.find_place(
            input="gas station",
            input_type="textquery",
            fields=['geometry', 'id'],
            location_bias=location_bias
        )["candidates"][0]["geometry"]["location"]  # {lat: ... , lnt: ...}


@dataclass(frozen=True)
class MatrixResponse:
    distance: int
    duration: int
    address: str
