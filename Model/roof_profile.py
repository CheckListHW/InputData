import numpy as np
from scipy.interpolate import griddata

from Model.json_in_out import JsonInOut
from Tools.geometry.nearst_dot import nearst_dot_index
from data_resource.digit_value import Limits


class RoofPoint(JsonInOut):
    __slots__ = 'x', 'y', 'z'

    def __init__(self, x: float = None, y: float = None, z: float = None, load_dict: dict = None):
        super().__init__(RoofPoint)
        self.x = x
        self.y = y
        self.z = z
        self.change(x, y, z)
        if load_dict:
            self.load_from_dict(load_dict)

    def change(self, x: float, y: float, z: float = None):
        self.x = x
        self.y = y
        self.z = z


class RoofProfile(JsonInOut):
    __slots__ = 'points', 'interpolate_method'

    def __init__(self):
        super().__init__(RoofProfile)
        self.interpolate_method = 'cubic'
        self.points: [RoofPoint] = list()

    def add(self, x: float, y: float, z: float):
        self.points.append(RoofPoint(x, y, z))

    def pop(self, x, y):
        index = nearst_dot_index([p.x for p in self.points], [p.y for p in self.points], x, y)
        if index in range(len(self.points)):
            self.points.pop(index)

    def load_from_dict(self, load_dict: dict):
        super(RoofProfile, self).load_from_dict(load_dict)
        self.points = []
        for point_dict in load_dict.get('points'):
            self.points.append(RoofPoint(load_dict=point_dict))

    def get_x_y(self) -> ([float], [float]):
        return [p.x for p in self.points], [p.y for p in self.points]

    def get_x_y_offset(self, base: float) -> [[float]]:
        points = np.array([[0, 0], [0, base], [base, 0], [base, base]] +
                          [[p.x/Limits.BASEPLOTSCALE*base, p.y/Limits.BASEPLOTSCALE*base] for p in self.points])
        val = np.array([0, 0, 0, 0] + [p.z for p in self.points])
        grid_x, grid_y = np.mgrid[0:base:1, 0:base:1]
        return griddata(points, val, (grid_x, grid_y), method=self.interpolate_method)
