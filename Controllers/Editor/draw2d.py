import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

from Model.surface2d import SurfaceFigure2d
from Tools.nearst_dot import nearst_dot_index, nearst_line_index
from Tools.draw_polygon_2d import draw_polygon
from Tools.dot_count_change import halve_dot_count


# x - width, y - length
class Edit2dSurface:
    def __init__(self, width: int = 25, length: int = 25, fig=None, ax=None):
        self.surface2d: SurfaceFigure2d
        self.line_dots_index: int
        self.nearst_dot_index: int = 0

        self.width = width if width in range(0, 501) else 25
        self.length = length if length in range(0, 501) else 25

        self.fig = fig if fig else plt.figure()
        self.ax = ax if ax else self.fig.add_subplot(111)

        self.plot_prepare()

    def plot_prepare(self):
        self.ax.set_xlim(0, self.length)
        self.ax.set_ylim(0, self.width)

        self.ax.xaxis.set_major_locator(MultipleLocator(self.length / 5))
        self.ax.yaxis.set_major_locator(MultipleLocator(self.width / 5))

        self.ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(5))

        self.ax.grid(which='major', color='#CCCCCC', linestyle='--')
        self.ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    def active_layer(self) -> SurfaceFigure2d:
        return self.surface2d

    def all_layers(self) -> [SurfaceFigure2d]:
        return [self.active_layer()]

    def set_active_layer(self, surf: SurfaceFigure2d):
        self.surface2d = surf

    def draw_line(self, x: [float], y: [float]):
        if not (x+y).__contains__(None):
            self.ax.plot(x, y, color='black', marker='.', markersize=6)

    def clear_content(self):
        for artist in self.ax.get_lines() + self.ax.collections:
            artist.remove()

        draw_polygon(0, 0, self.ax, size=max(self.width, self.length), color='white')

    def update_plot(self, fast: bool = False):
        if fast:
            self.clear_content()
        else:
            self.ax.clear()
            self.plot_prepare()
            self.ax.fill(self.active_layer().x_dots, self.active_layer().y_dots)

        for layer in self.all_layers():
            self.draw_curve(layer.x_dots, layer.y_dots)

    def halve_dot_count(self):
        self.active_layer().x_dots, self.active_layer().y_dots = \
            halve_dot_count(self.active_layer().x_dots, self.active_layer().y_dots)

        print(len(self.active_layer().x_dots), len(self.active_layer().y_dots))
        self.update_plot()

    def choose_dot(self, x: float, y: float):
        self.update_plot()
        self.nearst_dot_index = nearst_dot_index(self.active_layer().x_dots, self.active_layer().y_dots, x, y)

        try:
            x1, y1 = self.active_layer().x_dots[self.nearst_dot_index], self.active_layer().y_dots[self.nearst_dot_index]
            self.ax.scatter(x1, y1, color='red')
        except:
            pass

    def move_dot(self, x: float, y: float):
        self.active_layer().x_dots[self.nearst_dot_index] = x
        self.active_layer().y_dots[self.nearst_dot_index] = y

        self.update_plot(fast=True)

    def start_draw_curve(self, x: float, y: float):
        self.set_active_layer(SurfaceFigure2d())
        self.clear_content()
        self.active_layer().set_start_dot(x, y)

    def continue_draw_curve(self, x: float, y: float):
        self.draw_line([x, self.active_layer().pre_x], [y, self.active_layer().pre_y])
        self.active_layer().set_pre_dot(x, y)

    def end_draw_curve(self):
        lay = self.active_layer()
        self.draw_line([lay.start_x, lay.pre_x], [lay.start_y, lay.pre_y])
        self.active_layer().set_pre_dot(lay.start_x, lay.start_y)
        self.ax.fill(lay.x_dots, lay.y_dots)

    def delete_dot(self, x: float, y: float):
        if len(self.active_layer().x_dots) <= 1:
            self.active_layer().clear()
        else:
            self.choose_dot(x, y)
            self.active_layer().pop_dot(self.nearst_dot_index)

        self.update_plot()

    def choose_dots_beetwen_add(self, x: float, y: float):
        self.clear_content()
        self.draw_curve(self.active_layer().x_dots, self.active_layer().y_dots)

        _, self.line_dot_index = a, b = nearst_line_index(self.active_layer().x_dots, self.active_layer().y_dots, x, y)

        self.ax.scatter(self.active_layer().x_dots[a], self.active_layer().y_dots[a], color='red')
        self.ax.scatter(self.active_layer().x_dots[b], self.active_layer().y_dots[b], color='red')

    def add_dot(self, x, y):
        self.active_layer().insert_dot(self.line_dot_index, x, y)

        self.clear_content()
        self.draw_curve(self.active_layer().x_dots, self.active_layer().y_dots)

    def draw_curve(self, dots_x, dots_y):
        if dots_y and dots_x:
            self.draw_line(dots_x + [dots_x[0]], dots_y + [dots_y[0]])


if __name__ == "__main__":
    mPlt = Edit2dSurface(width=15, length=15)
    plt.show()
