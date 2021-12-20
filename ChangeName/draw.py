from abc import abstractmethod
from random import random

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

from ChangeName.Editor3d.draw_3d import DrawVoxels
from ChangeName.Editor3d.figure_3d import Figure3d

from ChangeName.Tools.plot_limit import PlotLimit

from ChangeName.Tools.nearst_dot import nearst_dot_index


# x - width, y - length, z - height
# Рисование работает следующим образом: В момент нажатия ЛКМ к событию движения мыжи
# привязывается handler с id self.release_event_id который рисует линии, после отпускания ЛКМ handler отвязывается
class PlotCustom:
    def __init__(self, size: int = None, width: int = 25, length: int = 25, height: int = 25, fig=None, ax=None):
        self.fig = fig if fig else plt.figure()
        self.ax = ax if ax else self.fig.add_subplot(111)

        self.set_limit(size, width, length, height)

        self.plot_prepare()

        self.release_event_id = None

    # Установка ограничений для плота
    def set_limit(self, s: int, w: int, l: int, h: int):
        if s in range(0, 501):
            self.length, self.width, self.height = s, s, s
            return

        self.width = w if w in range(0, 501) else 25
        self.height = h if h in range(0, 501) else 25
        self.length = l if l in range(0, 501) else 25

    # первичная настройк плота
    def plot_prepare(self):
        # Edit grid
        self.ax.set_xlim(0, self.length)
        self.ax.set_ylim(0, self.width)

        self.ax.xaxis.set_major_locator(MultipleLocator(self.length / 5))
        self.ax.yaxis.set_major_locator(MultipleLocator(self.width / 5))

        self.ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(5))

        self.ax.grid(which='major', color='#CCCCCC', linestyle='--')
        self.ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    def active_fig(self):
        return self.fig3d

    def draw_line(self, x: int, x1: int, y: int, y1: int):
        if not [x, x1, y, y1].__contains__(None):
            self.ax.plot([x, x1], [y, y1], color='black', marker='.', markersize=6)

    # Создает новую фигуру, устанавливает стартове значения, добавляет handler для движения мыши
    def clear_content(self):
        for artist in self.ax.get_lines() + self.ax.collections:
            artist.remove()
        self.ax.fill([0, 0, self.width, self.width, 0],
                                 [0, self.length, self.length, 0, 0],
                                 color='white')

    def choose_dot(self, x, y):
        self.nearst_dot_index = nearst_dot_index(self.fig3d.up.x_dots, self.fig3d.up.y_dots, x, y)

    def move_dot(self, x, y):
        self.fig3d.up.x_dots[self.nearst_dot_index] = x
        self.fig3d.up.y_dots[self.nearst_dot_index] = y
        self.draw_curve(self.fig3d.up.x_dots, self.fig3d.up.y_dots)

    def start_draw_curve(self, x, y):
        self.fig3d = Figure3d(height=self.height)
        self.clear_content()
        self.active_fig().up.set_start_dot(x, y)

    def continue_draw_curve(self, x, y):
        up = self.active_fig().up
        self.draw_line(x, up.pre_x, y, up.pre_y)
        up.set_pre_dot(x, y)

    def end_draw_curve(self):
        up = self.active_fig().up
        self.draw_line(up.start_x, up.pre_x, up.start_y, up.pre_y)
        self.ax.fill(up.x_dots, up.y_dots)

    def delete_dot(self, x, y):
        self.choose_dot(x, y)
        print(self.nearst_dot_index)

        xx = self.fig3d.up.x_dots.copy()
        self.fig3d.up.x_dots.pop(self.nearst_dot_index)
        self.fig3d.up.y_dots.pop(self.nearst_dot_index)
        print(self.fig3d.up.x_dots)
        for i in range(len(self.fig3d.up.x_dots)):
            print(i, self.fig3d.up.x_dots[i], xx[i])
        self.draw_curve(self.fig3d.up.x_dots, self.fig3d.up.y_dots)

    def add_dot(self):
        pass

    def show_3d_figure(self):
        DrawVoxels(self.fig3d, limits=PlotLimit(self.width, self.length, self.height))

    def draw_curve(self, x, y):
        self.clear_content()
        pre_x, pre_y = x[0], y[0]
        for i in range(1, len(x)):
            self.draw_line(x[i], pre_x, y[i], pre_y)
            pre_x, pre_y = x[i], y[i]


if __name__ == "__main__":
    mPlt = PlotCustom(width=15, length=15, height=1)
    plt.show()
