#! /usr/bin/env python3.10

# This file holds various classes and functions for Linear Algebra related stuff

from typing import NamedTuple, Tuple

class Coord(NamedTuple):
    x: float
    y: float
    z: float

    @staticmethod
    def of_str(coord_str: str):
        """
        This should be passed in a string like:
        (  17,   39,   68)
        """
        x, y, z = map(float, coord_str.replace('(', '').replace(')', '').strip().split(','))
        return Coord(x, y, z)

    @staticmethod
    def of(coord: Tuple[float, float, float]):
        """
        For easy construction out of a tuple
        """
        x, y, z = coord[0], coord[1], coord[2]
        return Coord(x, y, z)

    def euclidean_dist(self, other) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5

    def taxi_dist(self, other) -> float:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def __repr__(self) -> str:
        return f'Coord({self.x}, {self.y}, {self.z})'

