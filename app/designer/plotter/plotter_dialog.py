# python native modules

# third-party modules
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

# labtool project modules
from app.designer.plotter.plotter import Ui_Dialog


class PlotterDialog(QDialog, Ui_Dialog):

    def __init__(self, content: list, content_fields: list, *args, **kwargs):
        super(PlotterDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Instantiates the backend of the Figure plotter
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        self.preview.setCurrentIndex(self.preview.addWidget(self.canvas))

        # Internal members
        self.content = content
        self.content_fields = content_fields

        # Setting up the content of the Dialog
        self.x_channel.addItems(content_fields)
        self.y_channel.addItems(content_fields)

        # Connecting the slots and signals
        self.update.clicked.connect(self.on_update)

    ####################
    # GUI Dialog Slots #
    ####################
    def on_update(self):
        """ Updates the content of the Figure """
        if self.x_channel.currentText() != self.y_channel.currentText():
            x_data = [content_value[self.x_channel.currentText()] for content_value in self.content]
            y_data = [content_value[self.y_channel.currentText()] for content_value in self.content]

            self.axes.clear()
            self.axes.plot(x_data, y_data)

            self.axes.set_xscale("log")
            self.axes.minorticks_on()
            self.axes.grid(which="major")
            self.axes.grid(which="minor")

            self.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    dialog = PlotterDialog([], [])
    dialog.exec()
    app.exec()
