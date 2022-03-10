import math

import numpy as np
from matplotlib import pyplot as plt

from Controllers.qt_matplotlib_connector import EditorController
from Model.map import Map
from Model.shape import Shape
from Tools.geometry.point_in_polygon import check_polygon_in_polygon, check_point_in_polygon
from Tools.time_work import MyTimer


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

    def draw_all_polygon(self):
        self.plot3d.ax.clear()
        self.repeat = {}

        MyTimer.start()
        MyTimer.chek_start('shapes')
        shapes = self.map.get_visible_shapes()
        MyTimer.chek_finish('shapes')

        for shape in shapes:
            MyTimer.chek_start('calc_polygon_in_draw')
            data = self.calc_polygon_in_draw(shape)
            MyTimer.chek_finish('calc_polygon_in_draw')
            colors = np.empty(list(data.shape) + [4], dtype=np.float32)
            r, g, b = shape.color
            colors[:] = [r / 255, g / 255, b / 255, shape.alpha]
            self.plot3d.ax.voxels(data, facecolors=colors)

        MyTimer.finish()

        self.repeat = {}
        self.map.update_size()
        self.update_limits()
        self.plot3d.draw()
        self.all_polygon = np.zeros([1, 1, 1], dtype=bool)

    # set visible polygon
    def calc_polygon_in_draw(self, fig: Shape, ) -> []:
        x_size, y_size, z_size = self.map.size.x+1, self.map.size.y+1, max(fig.height, self.map.height_with_offset) + 1
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
                    MyTimer.chek_start('z1_offset')
                    z1_offset = int(lay_z + roof_profile_offset_x[y1])
                    MyTimer.chek_finish('z1_offset')
                    yy = [math.ceil(y1), math.ceil(y1), math.ceil(y1) + 1, math.ceil(y1) + 1]
                    MyTimer.chek_start('a')
                    # if check_polygon_in_polygon(x, y, xx, yy):
                    if check_point_in_polygon(x, y,  math.ceil(y1) + 0.5,  math.ceil(y1) + 0.5):
                        rep_name = "{0},{1},{2}".format(x1, y1, z1_offset)
                        if self.repeat.get(rep_name) is None:
                            self.repeat[rep_name] = data[x1, y1, z1_offset] = True
                    MyTimer.chek_finish('a')

        return data
