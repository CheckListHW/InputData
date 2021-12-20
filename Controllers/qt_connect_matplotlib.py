import enum
from random import random

import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backend_bases import MouseButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from ChangeName.Editor3d.plot_mode import *

from ChangeName.draw import PlotCustom


class MatplotlibConnector(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        FigureCanvasQTAgg.__init__(self, Figure(tight_layout=True))
        self.release_event_id = None
        self.toolbar = NavigationToolbar2QT(self, parent)

        self.mainLayout = QtWidgets.QGridLayout(parent)
        self.mainLayout.addWidget(self.toolbar)
        self.mainLayout.addWidget(self)

        self.ax = self.figure.add_subplot()
        self.plot = PlotCustom(width=15, length=15, height=1, fig=self.figure, ax=self.ax)

        self.set_mode(ModeStatus.DrawCurve)

        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('pick_event', self.pick_event)

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
        self.mode.on_click(event, self.mpl_connect)
        self.draw()

    def on_move(self, event):
        # self.mode.on_move(event)
        self.draw()

    def on_release(self, event):
        self.mode.on_release(event, self.mpl_disconnect)
        self.mpl_disconnect(self.handler_move_id)
        self.draw()
