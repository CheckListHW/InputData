from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from Controllers.edit_plot_modes import *
from Controllers.Editor.draw2d import Edit2dSurface


class MatplotlibConnector(FigureCanvasQTAgg):
    def __init__(self, parent=None, tight=False):
        if not tight:
            fig = Figure(tight_layout=True)
        else:
            fig = Figure()
            fig.subplots_adjust(left=-0.003, bottom=0, right=1, top=1, wspace=0, hspace=0)

        FigureCanvasQTAgg.__init__(self, fig)
        self.mainLayout = QtWidgets.QGridLayout(parent)
        self.mainLayout.addWidget(self)
        if not tight:
            self.mainLayout.addWidget(NavigationToolbar2QT(self, parent))

        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('pick_event', self.pick_event)

        self.ax = self.figure.add_subplot()
        self.plot = Edit2dSurface(width=15, length=15, fig=self.figure, ax=self.ax)

        self.set_mode(ModeStatus.DrawCurve)

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
        elif status == ModeStatus.Watch:
            self.mode = Watch(self.plot)

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

