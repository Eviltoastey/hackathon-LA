from __future__ import annotations

from dataclasses import dataclass

from googlemaps import Client


class GoogleClient:
    def __init__(self, google_client: Client) -> None:
        self._google_client = google_client

    def get_matrix_response(self, origin, destination, mode="driving") -> MatrixResponse:
        res = self._google_client.distance_matrix(origin, destination, mode)

        distance_value = res["rows"][0]["elements"][0]["distance"]["value"]
        duration_value = res["rows"][0]["elements"][0]["duration"]["value"]
        destination_address = res["destination_addresses"][0]

        return MatrixResponse(
            distance=distance_value,
            duration=duration_value,
            address=destination_address
        )


@dataclass(frozen=True)
class MatrixResponse:
    distance: int
    duration: int
    address: str
