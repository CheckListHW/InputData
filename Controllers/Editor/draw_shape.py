import numpy as np
from matplotlib import pyplot as plt

from Controllers.qt_matplotlib_connector import EditorController
from Model.map import Map
from Tools.point_in_polygon import check_point_in_polygon
from Model.shape import Shape


class Plot3d:
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
        x, y, z = self.map.size('x'), self.map.size('y'), self.map.size('z')
        if x:
            self.plot3d.ax.axes.set_xlim3d(xmin=0.000001, xmax=x)
        if y:
            self.plot3d.ax.axes.set_ylim3d(ymin=0.000001, ymax=y)
        if z:
            self.plot3d.ax.axes.set_zlim3d(zmin=0.000001, zmax=z)

    def draw_all_polygon(self):
        self.plot3d.ax.clear()
        self.update_limits()

        for shape in self.map.get_visible_shapes():
            data = self.calc_polygon_in_draw(shape)
            axes = [shape.size_x, shape.size_y, shape.height + 1]
            colors = np.empty(axes + [4], dtype=np.float32)
            r, g, b = shape.color
            colors[:] = [r / 255, g / 255, b / 255, shape.alpha]
            self.plot3d.ax.voxels(data, facecolors=colors)

        self.all_polygon = None
        self.plot3d.draw()

    # set visible polygon
    def calc_polygon_in_draw(self, fig: Shape) -> []:
        if self.all_polygon is None:
            self.all_polygon = np.zeros([fig.size_x, fig.size_y, fig.height + 1], dtype=bool)

        data = np.zeros([fig.size_x, fig.size_y, fig.height + 1], dtype=bool)
        for k in range(len(fig.layers)):
            for i in range(fig.size_x):
                x, y = fig.layers[k].curve
                for j in range(fig.size_y):
                    if check_point_in_polygon(x, y, i + 0.5, j + 0.5):
                        if not bool(self.all_polygon[i, j, fig.layers[k].z]):
                            data[i, j, fig.layers[k].z] = True
                            self.all_polygon[i, j, fig.layers[k].z] = True

        return data
