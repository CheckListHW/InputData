import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

from Model.surface2d import SurfaceFigure2d
from Tools.nearst_dot import nearst_dot_index, nearst_line_index
from Tools.draw_polygon_2d import draw_polygon
from Tools.dot_count_change import halve_dot_count


# x - width, y - length
class Edit2dSurface:
    def __init__(self, width: int = 25, length: int = 25, fig=None, ax=None):
        self.grid_off = False
        self.surface2d = SurfaceFigure2d()
        self.line_dots_index: int
        self.nearst_dot_index: int = 0

        self.width = width if width in range(0, 501) else 25
        self.length = length if length in range(0, 501) else 25

        self.fig = fig if fig else plt.figure()
        self.ax = ax if ax else self.fig.add_subplot(111)

        self.plot_prepare()

    def plot_prepare(self):
        if self.grid_off:
            return

        self.ax.set_xlim(0, self.length)
        self.ax.set_ylim(0, self.width)

        self.ax.xaxis.set_major_locator(MultipleLocator(self.length / 5))
        self.ax.yaxis.set_major_locator(MultipleLocator(self.width / 5))

        self.ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(5))

        self.ax.grid(which='major', color='#CCCCCC', linestyle='--')
        self.ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    def active_lay(self) -> SurfaceFigure2d:
        return self.surface2d

    def all_layers(self) -> [SurfaceFigure2d]:
        return [self.active_lay()]

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
            self.ax.fill(self.active_lay().x, self.active_lay().y)

        for lay in self.all_layers():
            self.draw_curve(lay.x, lay.y)

    def halve_dot_count(self):
        self.active_lay().x, self.active_lay().y = \
            halve_dot_count(self.active_lay().x, self.active_lay().y)

        print(len(self.active_lay().x), len(self.active_lay().y))
        self.update_plot()

    def choose_dot(self, x: float, y: float):
        self.update_plot()
        self.nearst_dot_index = nearst_dot_index(self.active_lay().x, self.active_lay().y, x, y)

        try:
            x1, y1 = self.active_lay().x[self.nearst_dot_index], self.active_lay().y[self.nearst_dot_index]
            self.ax.scatter(x1, y1, color='red')
        except:
            pass

    def move_dot(self, x: float, y: float):
        self.active_lay().x[self.nearst_dot_index] = x
        self.active_lay().y[self.nearst_dot_index] = y

        self.update_plot(fast=True)

    def start_draw_curve(self, x: float, y: float):
        self.set_active_layer(SurfaceFigure2d())
        self.clear_content()
        self.active_lay().set_start_dot(x, y)

    def continue_draw_curve(self, x: float, y: float):
        self.draw_line([x, self.active_lay().pre_x], [y, self.active_lay().pre_y])
        self.active_lay().set_pre_dot(x, y)

    def end_draw_curve(self):
        lay = self.active_lay()
        self.draw_line([lay.start_x, lay.pre_x], [lay.start_y, lay.pre_y])
        self.active_lay().set_pre_dot(lay.start_x, lay.start_y)
        self.ax.fill(lay.x, lay.y)

    def delete_dot(self, x: float, y: float):
        if len(self.active_lay().x) <= 1:
            self.active_lay().clear()
        else:
            self.choose_dot(x, y)
            self.active_lay().pop_dot(self.nearst_dot_index)

        self.update_plot()

    def choose_dots_beetwen_add(self, x: float, y: float):
        self.clear_content()
        self.draw_curve(self.active_lay().x, self.active_lay().y)

        _, self.line_dot_index = a, b = nearst_line_index(self.active_lay().x, self.active_lay().y, x, y)

        self.ax.scatter(self.active_lay().x[a], self.active_lay().y[a], color='red')
        self.ax.scatter(self.active_lay().x[b], self.active_lay().y[b], color='red')

    def add_dot(self, x, y):
        self.active_lay().insert_dot(self.line_dot_index, x, y)
        self.update_plot()

    def draw_curve(self, dots_x, dots_y):
        if dots_y and dots_x:
            self.draw_line(dots_x + [dots_x[0]], dots_y + [dots_y[0]])


if __name__ == "__main__":
    mPlt = Edit2dSurface(width=15, length=15)
    plt.show()
