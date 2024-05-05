import math
from collections import namedtuple
from typing import List

from .constants import KM_TO_METERS

Coordinates = namedtuple('Coordinates', ['latitude', 'longitude'])


class PointDistanceCalculator:

    EARTH_RADIUS_KM = 6371

    @staticmethod
    def calculate(point1: Coordinates, point2: Coordinates):

        dLat = (point2.latitude - point1.latitude) * math.pi / 180.0
        dLon = (point2.longitude - point1.longitude) * math.pi / 180.0

        lat1 = (point1.latitude) * math.pi / 180.0
        lat2 = (point2.latitude) * math.pi / 180.0

        haversine_formula_part = (
            pow(math.sin(dLat / 2), 2) +
            pow(math.sin(dLon / 2), 2) *
            math.cos(lat1) * math.cos(lat2)
        )
        dist_on_earth_in_radians = 2 * math.asin(
            math.sqrt(haversine_formula_part)
        )
        distance_on_earth_km = (
            PointDistanceCalculator.EARTH_RADIUS_KM * dist_on_earth_in_radians
        )
        return distance_on_earth_km * KM_TO_METERS

    @staticmethod
    def find_closest(
        target_point: Coordinates,
        other_points: List[Coordinates]
    ):
        min_distance = float('inf')
        closest_point = None
        for point in other_points:
            distance = PointDistanceCalculator.calculate(point, target_point)
            if distance < min_distance:
                min_distance = distance
                closest_point = point
        return closest_point, min_distance
