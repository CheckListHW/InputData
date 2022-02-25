from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from numpy.polynomial.polynomial import polyline

from Model.surface import Surface
from Tools.geometry.nearst_dot import nearst_dot_index, nearst_line_index, dot_to_border

# x - width, y - length
from Tools.geometry.simplify_line import simplify_line, polyline


def draw_polygon(x, y, ax, size=1, color='brown'):
    int_x, int_y = int(x), int(y)
    ax.fill([int_x, int_x + size, int_x + size, int_x, int_x],
            [int_y, int_y, int_y + size, int_y + size, int_y])#, color=color)


class EditSurface:
    __slots__ = 'ax', 'surface', 'grid_off', 'fig', 'nearst_dot_index', 'line_dot_index',

    def __init__(self, fig=None, ax=None):
        self.surface = Surface()
        self.grid_off, self.line_dot_index, self.nearst_dot_index = False, 999, 0

        self.fig = fig if fig else plt.figure()
        self.ax = ax if ax else self.fig.add_subplot(111)

        self.plot_prepare()

    def plot_prepare(self):
        self.ax.set_xlim(0, self.surface.base_scale)
        self.ax.set_ylim(0, self.surface.base_scale)

        if self.grid_off:
            return

        self.ax.xaxis.set_major_locator(MultipleLocator(self.surface.base_scale / 5))
        self.ax.yaxis.set_major_locator(MultipleLocator(self.surface.base_scale / 5))

        self.ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(5))

        self.ax.grid(which='major', color='#CCCCCC', linestyle='--')
        self.ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    def draw_line(self, x: [float], y: [float], color='black'):
        if not (x + y).__contains__(None):
            self.ax.plot(x, y, color=color, marker='.', markersize=6)

    def clear_content(self):
        for artist in self.ax.get_lines() + self.ax.collections:
            artist.remove()

        draw_polygon(0, 0, self.ax, size=self.surface.size.max(), color='white')

    def update_plot(self, fast: bool = False):
        if fast:
            self.clear_content()
        else:
            self.ax.clear()
            self.plot_prepare()
            x, y = self.surface.curve
            self.ax.fill(x, y)

        if self.surface.next_layer:
            x, y = self.surface.next_layer.curve
            self.ax.plot(x, y, color='green', linestyle='--')
            self.ax.fill(x, y, color='green', alpha=0.1)

        x, y = self.surface.curve
        self.draw_curve(x, y)

        if self.surface.prev_layer:
            x, y = self.surface.prev_layer.curve
            self.ax.plot(x, y, color='red')
            self.ax.fill(x, y, color='red', alpha=0.5)

        for split, color in zip(self.surface.splits, ['red', 'blue']):
            a, b = (split.a.x, split.a.y), (split.b.x, split.b.y)
            if a[0] is not None:
                a = (round(a[0] * self.surface.base_scale), round(a[1] * self.surface.base_scale))
                self.ax.scatter(a[0], a[1], color='red')
            if b[0] is not None:
                b = (round(b[0] * self.surface.base_scale), round(b[1] * self.surface.base_scale))
                self.ax.scatter(b[0], b[1], color='blue')
            if a[0] is not None and b[0] is not None:
                scale_x = self.surface.size.x / self.surface.base_scale
                scale_y = self.surface.size.y / self.surface.base_scale
                x, y = polyline(a, b, scale_x=scale_x, scale_y=scale_y)
                self.draw_line(x, y, color=color)

    def simplify_line(self, dot_count: int = None):
        x, y = self.surface.curve
        if dot_count:
            x, y = simplify_line(x, y, dot_count)
        else:
            x, y = simplify_line(x, y)
        self.surface.curve = x, y
        self.update_plot()

    def halve_dot_count(self):
        self.simplify_line(int(len(self.surface.curve[0]) / 2))
        self.update_plot()

    def choose_dot(self, x: float, y: float) -> Optional[int]:
        self.update_plot()
        dots_x, dots_y = self.surface.curve
        self.nearst_dot_index = nearst_dot_index(dots_x, dots_y, x, y)
        if self.nearst_dot_index is None:
            return None
        else:
            x1, y1 = dots_x[self.nearst_dot_index], dots_y[self.nearst_dot_index]
            self.ax.scatter(x1, y1, color='red')
            return self.nearst_dot_index

    def move_dot(self, x: float, y: float):
        if x and y:
            self.surface.dot_value_change(self.nearst_dot_index, x, y)
            self.update_plot(fast=True)

    def start_draw_curve(self, x: float, y: float):
        self.surface.clear()
        self.surface.set_start_dot(x, y)

    def continue_draw_curve(self, x: float, y: float):
        self.draw_line([x, self.surface.pre_x], [y, self.surface.pre_y])
        self.surface.set_pre_dot(x, y)

    def end_draw_curve(self):
        lay = self.surface
        self.draw_line([lay.start_x, lay.pre_x], [lay.start_y, lay.pre_y])
        self.surface.set_pre_dot(lay.start_x, lay.start_y)
        self.update_plot()

    def delete_dot(self, x: float, y: float):
        self.surface.pop_dot(self.choose_dot(x, y))
        self.update_plot()

    def choose_line(self, x: float, y: float):
        if self.surface.size.max() > 1:
            self.clear_content()
            dots_x, dots_y = self.surface.curve
            self.draw_curve(dots_x, dots_y)

            _, self.line_dot_index = a, b = nearst_line_index(dots_x, dots_y, x, y)
            try:
                self.ax.scatter(dots_x[a], dots_y[a], color='red')
                self.ax.scatter(dots_x[b], dots_y[b], color='red')
            except (IndexError, TypeError):
                print('choose_line', len(dots_x), len(dots_y), a, b)

    def add_split_dot(self, x1: float, y1: float, start_line: bool = True):
        x1, y1 = dot_to_border(x1, y1, self.surface.base_scale)
        self.surface.change_dot_split(x1 / self.surface.base_scale, y1 / self.surface.base_scale, start_line)
        self.update_plot()

    def add_dot(self, x, y):
        if x and y:
            if len(self.surface.x) < 1:
                self.start_draw_curve(x, y)
                self.end_draw_curve()
            else:
                self.surface.insert_dot(self.line_dot_index, x, y)
            self.update_plot()

    def draw_curve(self, dots_x, dots_y):
        if dots_y and dots_x:
            self.draw_line(dots_x + [dots_x[0]], dots_y + [dots_y[0]])


if __name__ == "__main__":
    mPlt = EditSurface()
    plt.show()
