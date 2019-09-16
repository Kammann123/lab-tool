"""
LabTool Graphic User-Interface (GUI) application
"""

# python native modules
import sys

# third-party modules
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

# labtool project modules
from app.designer.window import Ui_LabToolWindow

from labtool.tool import LabTool
from labtool.tool import BodeScale

from labtool.base.instrument import InstrumentType

from labtool.oscilloscope.base.oscilloscope import Sources
from labtool.oscilloscope.base.oscilloscope import Coupling
from labtool.oscilloscope.base.oscilloscope import TriggerMode
from labtool.oscilloscope.base.oscilloscope import TriggerSweep
from labtool.oscilloscope.base.oscilloscope import TriggerSlope
from labtool.oscilloscope.base.oscilloscope import Sources
from labtool.oscilloscope.base.oscilloscope import AcquireMode
from labtool.oscilloscope.base.oscilloscope import TimebaseMode


# Loading new available devices to use as Instruments...
from labtool.oscilloscope.agilent.agilent_dso6014 import AgilentDSO6014

from labtool.generator.agilent.agilent_33220a import Agilent33220A


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

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['log_callback'] = self.signals.log

    @pyqtSlot()
    def run(self):
        """ Initialise the runner function with passed args, kwargs. """
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class LabToolWindow(QMainWindow, Ui_LabToolWindow):

    def __init__(self, *args, **kwargs):
        super(LabToolWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Internal members of the LabToolWindow
        self.oscilloscope_devices = []
        self.generator_devices = []

        self.oscilloscope = None
        self.generator = None

        self.bode_measures = None

        # Mapping the widgets
        self.widget_map = {
            "DEVICE_CONNECTION": 0,
            "MEASURING_SETTINGS": 1,
            "MEASURE_OUTPUT": 2
        }

        # Slot and signal connection
        self.refresh.clicked.connect(self.refresh_devices)
        self.connection.clicked.connect(self.connect)

        self.settings_back.clicked.connect(self.return_connection)
        self.measure.clicked.connect(self.start_measuring)
        self.stop.clicked.connect(self.stop_measuring)
        self.measure_back.clicked.connect(self.return_setting)

        self.export_excel.clicked.connect(self.export)

        # ThreadPool
        self.thread_pool = QThreadPool()
        self.worker = None

        # Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.previewStack.setCurrentIndex(self.previewStack.addWidget(self.canvas))

    ##############################
    # Device Connection Routines #
    ##############################

    def connect(self):
        """ Connection establishment with devices """
        selected_oscilloscope_index = self.oscilloscopes.currentIndex()
        selected_generator_index = self.generators.currentIndex()
        self.oscilloscope = LabTool.open_device_by_id(self.oscilloscope_devices[selected_oscilloscope_index][0])
        self.generator = LabTool.open_device_by_id(self.generator_devices[selected_generator_index][0])
        self.stackedWidget.setCurrentIndex(self.widget_map["MEASURING_SETTINGS"])

    def refresh_devices(self):
        """ Refreshing the oscilloscope and generator devices list """
        # Cleaning up...
        self.oscilloscope_devices = []
        self.generator_devices = []
        self.oscilloscopes.clear()
        self.generators.clear()

        # Status flags
        excluded_devices = 0

        # Updating the oscilloscope and generator detected devices
        devices = LabTool.get_devices()
        for device in devices:
            device_info = LabTool.get_device_information(device)
            device_type = LabTool.is_device_detected(device_info)
            if device_type is InstrumentType.Generator:
                self.generator_devices.append([device, device_info])
            elif device_type is InstrumentType.Oscilloscope:
                self.oscilloscope_devices.append([device, device_info])
            else:
                excluded_devices += 1

        # Loading devices to the GUI List Widgets
        self.generators.addItems(
            [
                "{} - {} - {}".format(generator_info["brand"], generator_info["model"], generator_info["series-number"])
                for generator_id, generator_info in self.generator_devices
            ]
        )

        self.oscilloscopes.addItems(
            [
                "{} - {} - {}".format(osc_info["brand"], osc_info["model"], osc_info["series-number"])
                for osc_id, osc_info in self.oscilloscope_devices
            ]
        )

        # UserInterface messages
        if not len(devices):
            self.connection_status.setText(
                "No device connnections detected!"
            )
        elif excluded_devices:
            self.connection_status.setText(
                """{} device connection was excluded because the instrument was not detected.
                Only supported devices will be detected!""".format(
                    excluded_devices
                )
            )

        # Verifying if there are enough instruments selected to continue with the program
        self.connection.setEnabled(len(self.oscilloscope_devices) and len(self.generator_devices))

    ###############################
    # Measuring Settings Routines #
    ###############################

    def return_connection(self):
        """ Returns to the Device Connection step. """
        self.stackedWidget.setCurrentIndex(self.widget_map["DEVICE_CONNECTION"])

    def start_measuring(self):
        """ When Measure button is pressed, it validates settings are right and starts
        the algorithm, using both the oscilloscope and the generator selected. """

        # Input and Output channels cannot be the same!
        if self.input_source.currentText() == self.output_source.currentText():
            self.setting_status.setText("Input and Output channels cannot be the same...")
            return

        # Trigger with no channels!
        trigger_source = self.trigger_source.currentText()
        if trigger_source != self.input_source.currentText() and trigger_source != self.output_source.currentText():
            if trigger_source != Sources.External and trigger_source != Sources.Line:
                self.setting_status.setText("You're triggering without input, output, external or line sources...")
                return

        # Start frequency cannot be higher than stop frequency
        if self.start_frequency.value() >= self.stop_frequency.value():
            self.setting_status.setText("Start frequency is higher than stop frequency... really?")
            return

        # OK! No validation error detected, starting measuring process and going to the next
        # stage of the StackedWidget
        self.stackedWidget.setCurrentIndex(self.widget_map["MEASURE_OUTPUT"])
        self.stop.setEnabled(True)

        input_channel_setup = {
            "bandwidth_limit": self.input_bw.isChecked(),
            "coupling": LabTool.to_enum(self.input_coupling.currentText(), Coupling),
            "probe": int(self.input_probe.currentText()),
            "display": True,
            "range": 20,
            "offset": 0
        }

        output_channel_setup = {
            "bandwidth_limit": self.output_bw.isChecked(),
            "coupling": LabTool.to_enum(self.output_coupling.currentText(), Coupling),
            "probe": int(self.output_probe.currentText()),
            "display": True,
            "range": 20,
            "offset": 0
        }

        trigger_setup = {
            "trigger-mode": TriggerMode.Edge,
            "trigger-sweep": LabTool.to_enum(self.trigger_sweep.currentText(), TriggerSweep),
            "trigger-edge-level": float(self.trigger_level.value()),
            "trigger-edge-slope": LabTool.to_enum(self.trigger_slope.currentText(), TriggerSlope),
            "trigger-edge-source": LabTool.to_enum(self.trigger_source.currentText(), Sources),
            "hf-reject": self.trigger_hf_reject.isChecked(),
            "n-reject": self.trigger_n_reject.isChecked()
        }

        timebase_setup = {
            "timebase-mode": TimebaseMode.Main
        }

        acquire_setup = {
            "acquire-mode": AcquireMode.Average,
            "average-count": 2
        }

        bode_setup = {
            "delay": float(self.delay.value()),
            "stable-time": float(self.establishment_time.value()),
            "scale": LabTool.to_enum(self.scale.currentText(), BodeScale),
            "start-frequency": float(self.start_frequency.value()),
            "stop-frequency": float(self.stop_frequency.value()),
            "samples": int(self.samples.value())
        }

        generator_setup = {
            "amplitude": float(self.generator_vpp.value())
        }

        self.oscilloscope.reset()
        self.worker = Worker(
            LabTool.run_bode,
            self.oscilloscope, self.generator,
            bode_setup,
            generator_setup,
            trigger_setup,
            timebase_setup,
            acquire_setup,
            LabTool.to_enum(self.input_source.currentText(), Sources), input_channel_setup,
            LabTool.to_enum(self.output_source.currentText(), Sources), output_channel_setup
        )

        self.worker.signals.result.connect(self.measure_complete)
        self.worker.signals.log.connect(self.log_message)
        self.worker.signals.progress.connect(self.set_progress)
        self.thread_pool.start(self.worker)

    ###########################
    # Measure Output Routines #
    ###########################

    def log_message(self, value: str):
        """ Logging a message in the console of the Measure Output window state. """
        self.logger.setText(self.logger.toPlainText() + value)

    def set_progress(self, value: int):
        """ Setting the current progress of the measuring process. """
        self.progress.setValue(value)

    def measure_complete(self, result):
        """ Measure completed. """
        self.stop.setEnabled(False)
        self.measure_back.setEnabled(True)
        self.export_excel.setEnabled(True)
        self.bode_measures = result

        frequency = [measure["frequency"] for measure in self.bode_measures]
        module = [measure["bode-module"] for measure in self.bode_measures]
        phase = [measure["bode-phase"] for measure in self.bode_measures]

        self.figure.clear()

        module_axes = self.figure.add_subplot(
            1, 2, 1,
            title="Bode Module",
            xlabel="Frequency [Hz]",
            ylabel="|H(f)|dB"
        )

        phase_axes = self.figure.add_subplot(
            1, 2, 2,
            title="Bode Phase",
            xlabel="Frequency [Hz]",
            ylabel="H(f)°"
        )

        module_axes.minorticks_on()
        phase_axes.minorticks_on()

        module_axes.grid(b=True, which="both", axis="both")
        phase_axes.grid(b=True, which="both", axis="both")

        module_axes.semilogx(frequency, module)
        phase_axes.semilogx(frequency, phase)

        self.canvas.draw()

    def export(self):
        """ Exports measure data as excel file! """
        filepath = QFileDialog.getSaveFileName()[0]
        LabTool.export_to_csv(filepath, self.bode_measures)

    def return_setting(self):
        """ Returns to the setting widget view """
        self.measure_back.setEnabled(False)
        self.export_excel.setEnabled(False)
        self.stackedWidget.setCurrentIndex(self.widget_map["MEASURING_SETTINGS"])

    def stop_measuring(self):
        """ Stops the measuring process """
        self.stop.setEnabled(False)
        self.thread_pool.cancel(self.worker)
        self.worker = None
        self.stackedWidget.setCurrentIndex(self.widget_map["MEASURING_SETTINGS"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LabToolWindow()
    window.show()
    app.exec()
    LabTool.close_manager()
