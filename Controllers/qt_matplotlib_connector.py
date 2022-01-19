from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from Controllers.edit_plot_modes import *
from Controllers.Editor.draw2d import Edit2dSurface
from Model.surface_2d import SurfaceFigure2d


class MatplotlibConnector(FigureCanvasQTAgg):
    def __init__(self, mode: ModeStatus, surf: SurfaceFigure2d = None):
        # при добавлении 'super().__init__()' крашится

        self.ax = self.figure.add_subplot()
        self.plot = Edit2dSurface(width=15, length=15, fig=self.figure, ax=self.ax)
        print('---------------', surf, '---------------')

        self.plot.set_active_layer(surf)
        self.set_mode(mode)

        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('pick_event', self.pick_event)

    def change_lay(self, lay: SurfaceFigure2d):
        self.plot.surface = lay
        self.plot.update_plot()
        self.draw()

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
            self.mode = Watch(self.plot, self.kwargs.get('watch_click_handler'))

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


class MatplotlibConnectorTight(MatplotlibConnector):
    def __init__(self, parent=None, surf: SurfaceFigure2d = None, **kwargs):
        self.kwargs = kwargs
        fig = Figure()
        fig.subplots_adjust(left=-0.003, bottom=0, right=1, top=1, wspace=0, hspace=0)

        FigureCanvasQTAgg.__init__(self, fig)
        self.mainLayout = QtWidgets.QGridLayout(parent)
        self.mainLayout.addWidget(self)

        super().__init__(surf=surf, mode=ModeStatus.Watch)


class MatplotlibConnectorEdit(MatplotlibConnector):
    def __init__(self, parent=None, surf: SurfaceFigure2d = None, **kwargs):
        self.kwargs = kwargs
        fig = Figure(tight_layout=True)

        FigureCanvasQTAgg.__init__(self, fig)
        self.mainLayout = QtWidgets.QGridLayout(parent)
        self.mainLayout.addWidget(self)
        self.mainLayout.addWidget(NavigationToolbar2QT(self, parent))

        super().__init__(surf=surf, mode=ModeStatus.DrawCurve)


class MatplotlibConnector3dViewing(FigureCanvasQTAgg):
    def __init__(self, parent: QFrame):
        fig = Figure(tight_layout=True)

        FigureCanvasQTAgg.__init__(self, fig)
        self.mainLayout = QtWidgets.QGridLayout(parent)
        self.mainLayout.addWidget(self)
        self.mainLayout.addWidget(NavigationToolbar2QT(self, parent))
        self.ax = self.figure.add_subplot(111, projection='3d')
