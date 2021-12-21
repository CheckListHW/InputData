from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from Controllers.plot_mode import *
from Controllers.Editor.draw2d import Edit2dSurface


class MatplotlibConnector(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        FigureCanvasQTAgg.__init__(self, Figure(tight_layout=True))

        self.toolbar = NavigationToolbar2QT(self, parent)

        self.mainLayout = QtWidgets.QGridLayout(parent)
        self.mainLayout.addWidget(self.toolbar)
        self.mainLayout.addWidget(self)

        self.release_event_id = None
        self.ax = self.figure.add_subplot()
        self.plot = Edit2dSurface(width=15, length=15, fig=self.figure, ax=self.ax)

        self.set_mode(ModeStatus.DrawCurve)

        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('pick_event', self.pick_event)

    def halve_dot(self):
        self.plot.halve_dot_count()
        self.draw()

    def update_plot(self):
        self.plot.update_plot()
        self.draw()

    def set_mode(self, status: ModeStatus):
        if status == ModeStatus.DrawCurve:
            self.mode = DrawCurve(self.plot)
        elif status == ModeStatus.DeleteDot:
            self.mode = DeleteDot(self.plot)
        elif status == ModeStatus.AddDot:
            self.mode = AddDot(self.plot)
        elif status == ModeStatus.MoveDot:
            self.mode = MoveDot(self.plot)

    def on_click(self, event):
        self.handler_move_id = self.mpl_connect('motion_notify_event', self.on_move)
        self.mode.on_click(event)
        self.draw()

    def on_move(self, event):
        self.mode.on_move(event)
        self.draw()

    def on_release(self, event):
        self.mode.on_release(event)
        self.mpl_disconnect(self.handler_move_id)
        self.draw()
