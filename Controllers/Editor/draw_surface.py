import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

from Model.surface import Surface
from Tools.nearst_dot import nearst_dot_index, nearst_line_index
from Tools.draw_polygon_2d import draw_polygon

# x - width, y - length
from Tools.simplify_line import simplify_line


class EditSurface:
    def __init__(self, fig=None, ax=None):
        self.surface = Surface()
        self.grid_off, self.line_dot_index, self.nearst_dot_index = False, 999, 0

        self.fig = fig if fig else plt.figure()
        self.ax = ax if ax else self.fig.add_subplot(111)

        self.plot_prepare()

    def plot_prepare(self):
        self.ax.set_xlim(0, self.surface.size_x)
        self.ax.set_ylim(0, self.surface.size_y)

        if self.grid_off:
            return

        self.ax.xaxis.set_major_locator(MultipleLocator(self.surface.size_x / 5))
        self.ax.yaxis.set_major_locator(MultipleLocator(self.surface.size_y / 5))

        self.ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(5))

        self.ax.grid(which='major', color='#CCCCCC', linestyle='--')
        self.ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    def draw_line(self, x: [float], y: [float]):
        if not (x + y).__contains__(None):
            self.ax.plot(x, y, color='black', marker='.', markersize=6)

    def clear_content(self):
        for artist in self.ax.get_lines() + self.ax.collections:
            artist.remove()

        draw_polygon(0, 0, self.ax, size=max(self.surface.size_x, self.surface.size_y), color='white')

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

    def simplify_line(self, dot_count: int = None):
        x, y = self.surface.curve
        if dot_count:
            x, y = simplify_line(x, y, dot_count)
        else:
            x, y = simplify_line(x, y, self.surface.size())
        self.surface.curve = x, y
        self.update_plot()

    def halve_dot_count(self):
        self.simplify_line(int(self.surface.size() / 2))
        self.update_plot()

    def choose_dot(self, x: float, y: float):
        self.update_plot()
        dots_x, dots_y = self.surface.curve
        self.nearst_dot_index = nearst_dot_index(dots_x, dots_y, x, y)

        try:
            x1, y1 = dots_x[self.nearst_dot_index], dots_y.y[self.nearst_dot_index]
            self.ax.scatter(x1, y1, color='red')
        except:
            pass

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
        self.choose_dot(x, y)
        self.surface.pop_dot(self.nearst_dot_index)
        self.update_plot()

    def choose_line(self, x: float, y: float):
        if self.surface.size() > 1:
            self.clear_content()
            dots_x, dots_y = self.surface.curve
            self.draw_curve(dots_x, dots_y)

            _, self.line_dot_index = a, b = nearst_line_index(dots_x, dots_y, x, y)

            self.ax.scatter(dots_x[a], dots_y[a], color='red')
            self.ax.scatter(dots_x[b], dots_y[b], color='red')

    def add_dot(self, x, y):
        if x and y:
            if self.surface.size() < 1:
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
