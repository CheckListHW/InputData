import math

import numpy as np
from matplotlib import pyplot as plt

from mvc.Controller.qt_matplotlib_connector import EditorController
from mvc.Model.map import Map
from mvc.Model.shape import Shape
from utils.geometry.point_in_polygon import check_polygon_in_polygon
from utils.geometry.prepare_layers_for_plot_3d import data_for_plot_3d
from utils.transform_data_to_export import dict_update, transform_data


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
        x_size, y_size, z_size = self.map.size.x, self.map.size.y, self.map.size.z
        self.plot3d.ax.set_xlim3d(xmin=0.000001, xmax=x_size * 1.1)
        self.plot3d.ax.set_ylim3d(ymin=0.000001, ymax=y_size * 1.1)
        self.plot3d.ax.set_zlim3d(zmin=0.000001, zmax=z_size * 1.1)

    def redraw(self):
        if self.map.draw_speed == 'Polygon':
            self.draw_all_polygon()
        else:
            self.draw_plot()
        self.map.update_size()
        self.update_limits()
        self.plot3d.draw()

    def draw_plot(self):
        self.plot3d.ax.clear()
        shapes = self.map.get_visible_shapes()

        self.map.data = {}
        for fig in shapes:
            r_p_o = roof_profile_offset = self.map.roof_profile.get_x_y_offset(
                base=max(self.map.size.x, self.map.size.y))

            i_n_t = include_not_primary = True if self.map.draw_speed == 'Simple' else False

            layers = [lay for lay in fig.layers if (lay.primary or i_n_t) and lay.x != []]
            layers_x = [lay.scalable_curve[0] for lay in layers]

            if not layers_x:
                continue
            layers_y = [lay.scalable_curve[1] for lay in layers]

            layers_z = [
                [lay.z + r_p_o[int(x1)][int(y1)] for x1, y1 in zip(lay.scalable_curve[0], lay.scalable_curve[1])] for
                lay in layers]

            layers_x, layers_y, layers_z = data_for_plot_3d(layers_x, layers_y, layers_z)
            x, y, z = np.array(layers_x), np.array(layers_y), np.array(layers_z)
            color = '#%02x%02x%02x' % (fig.color[0], fig.color[1], fig.color[2])
            self.plot3d.ax.plot_surface(x, y, z, color=color, alpha=fig.alpha)

    def draw_all_polygon(self):
        self.plot3d.ax.clear()
        self.repeat, self.map.data, main_data, self.all_polygon = {}, {}, [], np.zeros([1, 1, 1], dtype=bool)
        for shape in self.map.get_visible_shapes():
            data = self.calc_polygon_in_draw(shape)
            self.map.data[f'{shape.name}|{shape.sub_name}'] = dict_update(self.map.data.get(shape.name),
                                                                          transform_data(data))
            colors = np.empty(list(data.shape) + [4], dtype=np.float32)
            r, g, b = shape.color
            colors[:] = [r / 255, g / 255, b / 255, shape.alpha]
            main_data.append((data, colors))
        self.draw(main_data)

    def draw(self, main_data: []):

        for (data, colors), i in zip(main_data, range(len(main_data))):
            self.plot3d.ax.voxels(data, facecolors=colors)

    # set visible polygon
    def calc_polygon_in_draw(self, fig: Shape) -> []:
        x_size, y_size, z_size = self.map.size.x, self.map.size.y, max(fig.height, self.map.height_with_offset) + 1
        roof_profile_offset = self.map.roof_profile.get_x_y_offset(base=max(self.map.size.x, self.map.size.y))
        data = np.zeros([x_size, y_size, z_size], dtype=bool)

        self.all_polygon.resize([max(x) for x in zip(data.shape, self.all_polygon.shape)])

        lay_size = fig.size.x * fig.size.y
        for lay in fig.layers:
            (x, y), lay_z = lay.scalable_curve, lay.z
            for x1 in range(fig.size.x):
                x1_c = math.ceil(x1)
                xx, rpo_x = [x1_c, x1_c + 1, x1_c, x1_c + 1], roof_profile_offset[x1]
                for y1 in range(fig.size.y):
                    y1_c = math.ceil(y1)
                    z1_offset, yy = int(lay_z + rpo_x[y1]), [y1_c, y1_c, y1_c + 1, y1_c + 1]
                    if check_polygon_in_polygon(x, y, xx, yy):
                        rep_name = lay_size * z1_offset + x1 * fig.size.y + y1
                        if self.repeat.get(rep_name) is None:
                            self.repeat[rep_name] = data[x1, y1, z1_offset] = True
        return data
