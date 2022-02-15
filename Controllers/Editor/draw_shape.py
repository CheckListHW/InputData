import sys
import time

import numpy as np
from matplotlib import pyplot as plt

from Controllers.qt_matplotlib_connector import EditorController
from Model.map import Map
from Tools.point_in_polygon import check_point_in_polygon
from Model.shape import Shape


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
        self.all_polygon = None
        self.plot3d = plot3d if plot3d else Plot3d()
        self.draw_all_polygon()

    def update_limits(self):
        size = self.map.size
        if size:
            self.plot3d.ax.set_xlim3d(xmin=0.000001, xmax=size.x * 1.1)
            self.plot3d.ax.set_ylim3d(ymin=0.000001, ymax=size.y * 1.1)
            self.plot3d.ax.set_zlim3d(zmin=0.000001, zmax=size.z * 1.1)

    def draw_all_polygon(self):
        self.plot3d.ax.clear()
        self.update_limits()

        for shape in self.map.get_visible_shapes():
            data = self.calc_polygon_in_draw(shape)
            axes = [shape.size.x, shape.size.y, shape.height + 1]
            colors = np.empty(axes + [4], dtype=np.float32)
            r, g, b = shape.color
            colors[:] = [r / 255, g / 255, b / 255, shape.alpha]
            self.plot3d.ax.voxels(data, facecolors=colors)

        self.all_polygon = None
        self.plot3d.draw()

    # set visible polygon
    def calc_polygon_in_draw(self, fig: Shape) -> []:
        if self.all_polygon is None:
            self.all_polygon = np.zeros([self.map.size.x, self.map.size.y, fig.height+1], dtype=bool)

        data = np.zeros([fig.size.x, fig.size.y, fig.height + 1], dtype=bool)
        self.all_polygon.resize([max(x) for x in zip(data.shape, self.all_polygon.shape)])

        for k in range(len(fig.layers)):
            for x1 in range(fig.size.x):
                x, y = fig.layers[k].scalable_curve
                z1 = fig.layers[k].z
                for y2 in range(fig.size.y):
                    result = check_point_in_polygon(x, y, x1 + 0.5, y2 + 0.5) and not bool(self.all_polygon[x1, y2, z1])
                    data[x1, y2, z1] = self.all_polygon[x1, y2, z1] = result

        return data
