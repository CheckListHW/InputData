import numpy as np
from matplotlib import pyplot as plt

from Model.map import Map
from Tools.point_in_polygon import point_in_polygon
from Tools.plot_limit import PlotLimit
from Model.figure_3d import Figure3d

debug_mode = False


class Plot3d:
    def __init__(self, fig: plt.figure = None, ax: plt.axes = None):
        if not fig or not ax:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            self.fig = fig
            self.ax = ax


class DrawVoxels:
    def __init__(self, map_val: Map, plot3d=None, limits: PlotLimit = None):
        self.map = map_val
        self.plot3d = plot3d if plot3d else Plot3d()
        self.limits = limits
        self.set_limits()

        self.draw_all_polygon()

    def set_limits(self):
        if not self.limits:
            self.limits = PlotLimit(x=15, y=15, z=15)
        if self.limits.x:
            self.plot3d.ax.axes.set_xlim3d(xmin=0.000001, xmax=self.limits.x)
        if self.limits.y:
            self.plot3d.ax.axes.set_ylim3d(ymin=0.000001, ymax=self.limits.y)
        if self.limits.z:
            self.plot3d.ax.axes.set_zlim3d(zmin=0.000001, zmax=self.limits.z)

    def draw_all_polygon(self):
        for fig in self.map.get_figures():
            data = self.calc_polygon_in_draw(fig)
            axes = fig.size_fig()
            colors = np.empty(axes + [4], dtype=np.float32)
            r, g, b = fig.get_color()
            colors[:] = [r / 255, g / 255, b / 255, 0.9]
            self.plot3d.ax.voxels(data, facecolors=colors)

    "Delete invisible polygon"

    def calc_polygon_in_draw(self, fig: Figure3d):
        data = np.zeros(fig.size_fig(), dtype=bool)
        layers = fig.get_layers_by_z()
        for lay in layers:
            print(lay.z)
        for k in range(len(layers)):
            for i in range(fig.size_x()):
                for j in range(fig.size_y()):
                    if point_in_polygon(layers[k].x, layers[k].y,
                                        i + 0.5, j + 0.5):
                        data[i, j, layers[k].z] = True
        return data

    def update(self):
        self.plot3d.ax.clear()
        self.set_limits()
        self.draw_all_polygon()
