import numpy as np
from matplotlib import pyplot as plt
from ChangeName.Tools.point_in_polygon import point_in_polygon
from ChangeName.Tools.plot_limit import PlotLimit
from ChangeName.Editor3d.figure_3d import Figure3d

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
    def __init__(self, fig3d: Figure3d, plot3d=None, limits: PlotLimit = None):
        self.fig3d = fig3d
        self.plot3d = plot3d if plot3d else Plot3d()
        self.set_limits(limits)

        self.draw_all_polygon()
        plt.show()

    def set_limits(self, limits: PlotLimit):
        if limits.x:
            self.plot3d.ax.axes.set_xlim3d(xmin=0.000001, xmax=limits.x)
        if limits.y:
            self.plot3d.ax.axes.set_ylim3d(ymin=0.000001, ymax=limits.y)
        if limits.z:
            self.plot3d.ax.axes.set_zlim3d(zmin=0.000001, zmax=limits.z)

    def clean_figure(self, data):
        new_data = data.copy()

        for i in range(1, len(self.X) - 1):
            for j in range(1, len(self.Y) - 1):
                for k in range(1, len(self.Z) - 1):
                    if data[i, j, k]:
                        if data[i - 1, j, k] and data[i, j - 1, k] and \
                                data[i + 1, j, k] and data[i, j + 1, k]:
                            new_data[i, j, k] = False
        return new_data

    def draw_all_polygon(self):
        # data = self.clean_figure(self.calc_polygon_in_draw())
        data = self.calc_polygon_in_draw()

        axes = self.fig3d.size_fig()
        colors = np.empty(axes + [4], dtype=np.float32)
        colors[:] = [1, 0, 0, 0.9]

        self.plot3d.ax.voxels(data, facecolors=colors)
        plt.show()

    "Delete invisible polygon"
    def calc_polygon_in_draw(self):
        print(len(self.fig3d.layers))
        data = np.zeros(self.fig3d.size_fig(), dtype=bool)
        for k in range(len(self.fig3d.layers)):
            for i in range(self.fig3d.size_x()):
                for j in range(self.fig3d.size_y()):
                    if point_in_polygon(self.fig3d.layers[k].x_dots, self.fig3d.layers[k].y_dots,
                                        i + 0.5, j + 0.5):
                        data[i, j, k] = True
        return data
