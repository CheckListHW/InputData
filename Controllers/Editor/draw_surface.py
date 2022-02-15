from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

from Model.surface import Surface
from Tools.nearst_dot import nearst_dot_index, nearst_line_index
from Tools.draw_polygon_2d import draw_polygon

# x - width, y - length
from Tools.simplify_line import simplify_line
from Tools.counter import Counter

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
        a, b = self.surface.split_line
        if a and b:
            self.draw_line([a[0], b[0]], [a[1], b[1]], color='red')

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
        print('self.nearst_dot_index', self.nearst_dot_index)
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
        print(self.choose_dot(x, y))
        print('delete dot', Counter.step())
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
                print(len(dots_x), len(dots_y), a, b)

    def add_split_dot(self, x1: float, y1: float):
        a, b = self.surface.split_line
        x, y = self.surface.curve
        i = nearst_dot_index(x, y, x1, y1)
        a, b = self.surface.split_line = b, (x[i], y[i])
        if a and b:
            self.draw_line([a[0], b[0]], [a[1], b[1]], color='red')
        self.choose_dot(x1, y1)

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
