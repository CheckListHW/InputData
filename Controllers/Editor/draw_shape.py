import math
from typing import List

import numpy as np
from matplotlib import pyplot as plt

from Controllers.qt_matplotlib_connector import EditorController
from Model.map import Map
from Model.shape import Shape
from Tools.geometry.point_in_polygon import check_polygon_in_polygon, check_point_in_polygon


class Plot3d:
    __slots__ = 'fig', 'ax', 'connector'

    def __init__(self, connector: EditorController = None):
        if connector is None:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            self.connector = connector
            self.fig = connector.figure
            self.ax = connector.ax

    def draw(self):
        if hasattr(self, 'connector'):
            self.connector.draw()


class DrawVoxels:
    def __init__(self, map_val: Map, plot3d=None):
        self.map = map_val
        self.all_polygon = np.zeros([1, 1, 1], dtype=bool)
        self.plot3d = plot3d if plot3d else Plot3d()

    def update_limits(self):
        x_size, y_size, z_size = self.all_polygon.shape
        self.plot3d.ax.set_xlim3d(xmin=0.000001, xmax=x_size * 1.1)
        self.plot3d.ax.set_ylim3d(ymin=0.000001, ymax=y_size * 1.1)
        self.plot3d.ax.set_zlim3d(zmin=0.000001, zmax=z_size * 1.1)

    def transform_data(self, data: []) -> dict:
        map_dict = {}
        for i in range(len(data)):
            map_dict[i] = {}
            for j in range(len(data[i])):
                start = False
                map_dict[i][j] = []
                for k in range(len(data[i][j])):

                    if data[i][j][k] and not start:
                        start = True
                        map_dict[i][j].append({'s': k, 'e': len(data[i][j])})
                    elif not data[i][j][k] and start:
                        start = False
                        map_dict[i][j][-1]['e'] = k - 1
                if not map_dict[i][j]:
                    map_dict[i].pop(j)
                # if i == 15 and j == 14:
                #     print(map_dict[i][j])
            if map_dict[i] == {}:
                map_dict.pop(i)
        return map_dict

    def dict_update(self, old: dict, new: dict) -> dict:
        if old and new:
            for i in set(list(old.keys())+list(new.keys())):
                if old.get(i) is not None:
                    if new.get(i) is not None:
                        if type(old[i]) in [list]:
                            old[i] += new[i]
                        else:
                            self.dict_update(old[i], new[i])
                        # for j in set(list(old[i].keys()) + list(new[i].keys())):
                        #     if old[i].get(j) is not None:
                        #         if new[i].get(j) is not None:
                        #             old[i][j] += new[i][j]
                        #     else:
                        #         old[i][j] = new[i][j]
                else:
                    old[i] = new[i]
            return old
        else:
            return new

    def draw_all_polygon(self):
        self.plot3d.ax.clear()
        self.repeat = {}

        shapes = self.map.get_visible_shapes()

        for shape in shapes:
            data = self.calc_polygon_in_draw(shape)
            print(shape.name + shape.sub_name)
            self.map.data[shape.name] = self.dict_update(self.map.data.get(shape.name), self.transform_data(data))
            colors = np.empty(list(data.shape) + [4], dtype=np.float32)
            r, g, b = shape.color
            colors[:] = [r / 255, g / 255, b / 255, shape.alpha]
            self.plot3d.ax.voxels(data, facecolors=colors)

        self.repeat = {}
        self.map.update_size()
        self.update_limits()
        self.plot3d.draw()
        self.all_polygon = np.zeros([1, 1, 1], dtype=bool)

    # set visible polygon
    def calc_polygon_in_draw(self, fig: Shape, ) -> []:
        x_size, y_size, z_size = self.map.size.x, self.map.size.y, max(fig.height, self.map.height_with_offset) + 1
        roof_profile_offset = self.map.roof_profile.get_x_y_offset(base=max(self.map.size.x, self.map.size.y))
        data = np.zeros([x_size, y_size, z_size], dtype=bool)

        self.all_polygon.resize([max(x) for x in zip(data.shape, self.all_polygon.shape)])

        for k in range(len(fig.layers)):
            x, y = fig.layers[k].scalable_curve
            lay_z = fig.layers[k].z
            for x1 in range(fig.size.x):
                xx = [math.ceil(x1), math.ceil(x1) + 1, math.ceil(x1), math.ceil(x1) + 1]
                roof_profile_offset_x = roof_profile_offset[x1]
                for y1 in range(fig.size.y):
                    z1_offset = int(lay_z + roof_profile_offset_x[y1])
                    yy = [math.ceil(y1), math.ceil(y1), math.ceil(y1) + 1, math.ceil(y1) + 1]
                    if check_polygon_in_polygon(x, y, xx, yy):
                        rep_name = "{0},{1},{2}".format(x1, y1, z1_offset)
                        if self.repeat.get(rep_name) is None:
                            self.repeat[rep_name] = data[x1, y1, z1_offset] = True

        return data
