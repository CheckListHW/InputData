import enum
from abc import ABC, abstractmethod

from matplotlib.backend_bases import MouseButton

from ChangeName.draw import PlotCustom


class ModeStatus(enum.Enum):
    DrawCurve = 1
    DeleteDot = 2
    AddDot = 3
    MoveDot = 4


class Mode:
    def __init__(self, plot: PlotCustom):
        self.handler_move_id = None
        self.plot = plot

    @abstractmethod
    def on_click(self, event, mpl_connect):
        """handler on click"""

    @abstractmethod
    def on_move(self, event):
        """handler on move"""

    @abstractmethod
    def on_release(self, event, mpl_connect):
        """handler on release"""


class DrawCurve(Mode):
    def on_click(self, event, mpl_connect):
        self.handler_move_id = mpl_connect('motion_notify_event', self.on_move)
        if event.button is MouseButton.LEFT:
            self.plot.start_draw_curve(event.xdata, event.ydata)
            pass

    def on_move(self, event):
        
        if event.button is MouseButton.LEFT:
            if event.inaxes:
                self.plot.continue_draw_curve(event.xdata, event.ydata)

    def on_release(self, event, disconnect):
        disconnect(self.handler_move_id)
        if event.button is MouseButton.LEFT:
            self.plot.end_draw_curve()


class DeleteDot(Mode):
    def on_click(self, event, mpl_connect):
        self.plot.delete_dot(event.x, event.y)
        pass

    def on_move(self, event):
        pass

    def on_release(self, event, mpl_connect):
        pass


class AddDot(Mode):
    def on_click(self, event, mpl_connect):
        pass

    def on_move(self, event):
        pass

    def on_release(self, event, mpl_connect):
        pass


class MoveDot(Mode):
    def on_click(self, event, mpl_connect):
        if event.button is MouseButton.LEFT:
            self.plot.choose_dot(event.xdata, event.ydata)
        if event.button is MouseButton.RIGHT:
            self.plot.move_dot(event.xdata, event.ydata)

    def on_move(self, event):
        pass

    def on_release(self, event, mpl_connect):
        pass
