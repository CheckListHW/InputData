import enum
from abc import abstractmethod
from typing import Callable

from matplotlib.backend_bases import MouseButton

from Controllers.Editor.draw_surface import EditSurface


class ModeStatus(enum.Enum):
    DrawCurve = 1
    DeleteDot = 2
    AddDot = 3
    MoveDot = 4
    Watch = 5


class Mode:
    __slots__ = ['handler_move_id', 'plot']

    def __init__(self, plot: EditSurface):
        self.handler_move_id: int
        self.plot: EditSurface = plot

    @abstractmethod
    def on_click(self, event):
        """handler on click"""

    @abstractmethod
    def on_move(self, event):
        """handler on move"""

    @abstractmethod
    def on_release(self, event):
        """handler on release"""


class DrawCurve(Mode):
    def on_click(self, event):
        if event.button is MouseButton.LEFT:
            self.plot.start_draw_curve(event.xdata, event.ydata)

    def on_move(self, event):
        if event.button is MouseButton.LEFT:
            if event.inaxes:
                self.plot.continue_draw_curve(event.xdata, event.ydata)

    def on_release(self, event):
        if event.button is MouseButton.LEFT:
            self.plot.end_draw_curve()


class DeleteDot(Mode):
    def on_click(self, event):
        if event.button is MouseButton.LEFT:
            self.plot.choose_dot(event.xdata, event.ydata)
        if event.button is MouseButton.RIGHT:
            self.plot.delete_dot(event.xdata, event.ydata)

    def on_move(self, event):
        pass

    def on_release(self, event):
        pass


class AddDot(Mode):
    def on_click(self, event):
        if event.button is MouseButton.LEFT:
            self.plot.choose_line(event.xdata, event.ydata)
        if event.button is MouseButton.RIGHT:
            self.plot.add_dot(event.xdata, event.ydata)

    def on_move(self, event):
        pass

    def on_release(self, event):
        pass


class MoveDot(Mode):
    def on_click(self, event):
        if event.button is MouseButton.LEFT:
            self.plot.choose_dot(event.xdata, event.ydata)
        if event.button is MouseButton.RIGHT:
            self.plot.move_dot(event.xdata, event.ydata)

    def on_move(self, event):
        self.plot.move_dot(event.xdata, event.ydata)

    def on_release(self, event):
        self.plot.update_plot()


class Watch(Mode):
    def __init__(self, plot, click_handler: Callable = None):
        super(Watch, self).__init__(plot)
        self.plot.grid_off = True
        self.plot.update_plot()
        self.move_handler = click_handler

    def on_click(self, event):
        if self.move_handler:
            self.move_handler()

    def on_move(self, event):
        pass

    def on_release(self, event):
        pass
