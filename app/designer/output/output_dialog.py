# python native modules

# third-party modules
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pandas

# labtool project modules
from app.designer.output.output import Ui_Dialog
from app.designer.plotter.plotter_dialog import PlotterDialog

from labtool.algorithm.base.measure_algorithm import MeasureAlgorithm


class WorkerSignals(QObject):
    """ Defines the signals available from a running worker thread.

    Supported signals are:
        + finished: No data is sent
        + error: tuple (exctype, value, traceback.format_exc() )
        + result: `object` data returned from processing, anything
        + progress: int indicating % progress
        + log: str logging notificatons
    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    log = pyqtSignal(str)


class Worker(QRunnable):
    """ Worker Thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.stopped = False
        self.fn.reset()

        # Add the callback to our kwargs
        self.fn.progress_callback = self.signals.progress
        self.fn.log_callback = self.signals.log

    @pyqtSlot()
    def stop(self):
        self.stopped = True

    @pyqtSlot()
    def run(self):
        """ Initialise the runner function with passed args, kwargs. """
        # Retrieve args/kwargs here; and fire processing using them
        try:
            while not self.stopped:
                if not self.fn.finished:
                    self.fn(*self.args, **self.kwargs)
                else:
                    self.signals.result.emit(self.fn.get_result())
                    break
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()  # Done


class OutputDialog(QDialog, Ui_Dialog):

    def __init__(self, algorithm=None, *args, **kwargs):
        super(OutputDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Output Dialog")
        self.setFixedSize(self.size())

        # OutputDialog Members
        self.algorithm = algorithm
        self.worker = None
        self.pool = QThreadPool()

        self.result_fields = []
        self.results = []

        # Slot and Signal connection
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        self.reset_button.clicked.connect(self.on_reset)

        self.excel_button.clicked.connect(self.on_excel)
        self.plot.clicked.connect(self.on_plot)

    ######################################
    # GUI Output Dialog Internal Methods #
    ######################################
    def start(self):
        """ Starts the algorithm process """
        if self.worker is None:
            self.worker = Worker(self.algorithm)

            self.worker.signals.progress.connect(self.set_progress)
            self.worker.signals.result.connect(self.set_results)
            self.worker.signals.log.connect(self.set_status)

            self.pool.start(self.worker)

    def stop(self):
        """ Stops the algorithm process """
        if self.worker is not None:
            self.worker.stop()
            self.worker = None

    def reset(self):
        """ Resets the algorithm process """
        self.stop()
        self.start()

    ###########################
    # GUI Output Dialog Slots #
    ###########################
    def on_stop(self):
        """ Stops the measuring process """
        self.stop()

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(False)

    def on_start(self):
        """ Starts the measuring process """
        self.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.reset_button.setEnabled(True)

    def on_reset(self):
        """ Resets the measuring process """
        self.reset()

    def on_excel(self):
        """ Exports the excel file """
        # Opening where the excel is going to be saved
        filepath = QFileDialog.getSaveFileName()[0]

        # Formatting data to be saved in the excel
        dictionary = {field: [] for field in self.result_fields}
        for field in dictionary.keys():
            for result in self.results:
                dictionary[field].append(result[field])
        dataframe = pandas.DataFrame(dictionary)

        # Saving the excel file
        writer = pandas.ExcelWriter("{}.xlsx".format(filepath), engine="xlsxwriter")
        dataframe.to_excel(writer, sheet_name="Measure Output")
        writer.save()

    def on_plot(self):
        """ Open the plot dialog """
        plotter_dialog = PlotterDialog(self.results, self.result_fields)
        plotter_dialog.exec()

    ###############################
    # GUI Output Dialog Interface #
    ###############################
    def set_status(self, status: str):
        """ Sets the status message on the Output Dialog """
        self.status.setText(status)

    def set_progress(self, progress: int):
        """ Sets the current progress value on the Output Dialog """
        self.progress.setValue(progress)

    def set_results(self, results: list):
        """ Sets the list of samples defined as dictionaries """
        if results is not None:
            # Save current result values
            self.results = results
            self.result_fields = self.results[0].keys()

            # Set the sample field of the GUI
            self.samples.setValue(len(self.results))

            # Set the fields of the GUI
            self.fields.clear()
            self.fields.addItems(self.result_fields)

            # Enables the buttons
            self.excel_button.setEnabled(True)
            self.plot.setEnabled(True)


if __name__ == "__main__":
    app = QApplication([])
    dialog = OutputDialog()
    dialog.exec()
    app.exec()
