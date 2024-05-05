from typing import List

from .constants import ID_KEY, LATITUDE_KEY, LONGITUDE_KEY
from .descriptors import URLDesc
from .http_client import HTTPClient
from .point_distance_calculator import Coordinates, PointDistanceCalculator
from .vehicle import Vehicle


class VehicleManager:

    base_url = URLDesc()

    def __init__(self, url: str, path_segment: str = 'vehicles') -> None:

        self.base_url = url
        self.path_segment = path_segment
        self.url_string = '/'.join((self.base_url, self.path_segment))

        self._client = HTTPClient()

    def get_vehicles(self) -> List[Vehicle]:
        data = self._get_all_vehicle()

        response = [Vehicle(**row) for row in data]
        return response

    def filter_vehicles(self, params: dict) -> List[Vehicle]:
        response = list()

        list_of_veh_data = self._get_all_vehicle()
        list_of_filter_items = params.items()

        for veh_data in list_of_veh_data:
            veh_data_items = veh_data.items()
            for filter_item in list_of_filter_items:
                if filter_item not in veh_data_items:
                    break
            else:
                response.append(Vehicle(**veh_data))

        return response

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        data = self._get_vehicle_by_id(vehicle_id)
        return Vehicle(**data)

    def add_vehicle(self, vehicle: Vehicle) -> None:
        dict_vehicle = vehicle.get_dict_repr_except_id()
        self._create_vehicle(dict_vehicle)

    def update_vehicle(self, vehicle: Vehicle) -> None:
        dict_vehicle = vehicle.get_dict_repr_except_id()
        self._put_vehicle_by_id(vehicle.id, dict_vehicle)

    def delete_vehicle(self, id: int) -> None:
        self._delete_vehicle_by_id(id)

    def get_distance(self, id1: int, id2: int) -> float:
        vehicle_1 = self._get_vehicle_by_id(id1)
        vehicle_2 = self._get_vehicle_by_id(id2)

        vehicle_1_coord = Coordinates(
            latitude=vehicle_1[LATITUDE_KEY],
            longitude=vehicle_1[LONGITUDE_KEY]
            )

        vehicle_2_coord = Coordinates(
            latitude=vehicle_2[LATITUDE_KEY],
            longitude=vehicle_2[LONGITUDE_KEY]
            )

        return PointDistanceCalculator.calculate(
            vehicle_1_coord,
            vehicle_2_coord
        )

    def get_nearest_vehicle(self, id: int) -> Vehicle:
        all_vehicle = self._get_all_vehicle()
        points_to_vehicle_dict = dict()

        for vehicle in all_vehicle:
            if vehicle[ID_KEY] == id:
                target_points = Coordinates(
                    latitude=vehicle[LATITUDE_KEY],
                    longitude=vehicle[LONGITUDE_KEY]
                )
            else:
                points_to_vehicle_dict[
                    Coordinates(
                        latitude=vehicle[LATITUDE_KEY],
                        longitude=vehicle[LONGITUDE_KEY]
                    )
                ] = vehicle
        closet_point, _ = PointDistanceCalculator.find_closest(
                target_points,
                list(points_to_vehicle_dict.keys())
            )
        return Vehicle(**points_to_vehicle_dict[closet_point])

    def _get_url_with_id(self, id: int) -> str:
        return '/'.join((self.url_string, str(id)))

    def _get_all_vehicle(self) -> List[dict]:
        return self._client.get(self.url_string).json()

    def _get_vehicle_by_id(self, id: int) -> dict:
        url_string = self._get_url_with_id(id)
        return self._client.get(url_string).json()

    def _put_vehicle_by_id(self, id: int, data: dict) -> None:
        url_string = self._get_url_with_id(id)
        self._client.put(url_string, data)

    def _delete_vehicle_by_id(self, id: int) -> None:
        url_string = self._get_url_with_id(id)
        self._client.delete(url_string)

    def _create_vehicle(self, data: dict) -> None:
        self._client.post(self.url_string, data)
