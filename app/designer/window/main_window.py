# python native modules

# third-party modules
from PyQt5.QtWidgets import *

# labtool project modules
from app.designer.window.window import Ui_LabToolWindow
from app.designer.oscilloscope_settings.oscilloscope_settings_dialog import OscilloscopeSettingsDialog
from app.designer.generator_settings.generator_settings_dialog import GeneratorSettingsDialog
from app.designer.impedance.impedance_dialog import ImpedanceDialog
from app.designer.bode.bode_dialog import BodeDialog
from app.designer.output.output_dialog import OutputDialog

from labtool.algorithm.bode_algorithm import BodeAlgorithm
from labtool.algorithm.impedance_algorithm import ImpedanceAlgorithm

from labtool.base.instrument import InstrumentType
from labtool.tool import LabTool

# Installing devices...(?)
from labtool.oscilloscope.agilent.agilent_dso6014A import AgilentDSO6014A
from labtool.oscilloscope.agilent.agilent_dso7014A import AgilentDSO7014A
from labtool.oscilloscope.rigol.rigol_ds4014 import RigolDS4014

from labtool.generator.agilent.agilent_33220a import Agilent33220A


class MainWindow(QMainWindow, Ui_LabToolWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("LabTool")
        self.setFixedSize(self.size())

        # MainWindow internal members
        self.widget_map = {
            "DEVICE_CONNECTION": 0,
            "MAIN_MENU": 1
        }

        self.connected_devices = []
        self.oscilloscope = None
        self.generator = None

        # Children Dialogs
        self.oscilloscope_settings_dialog = OscilloscopeSettingsDialog()
        self.generator_settings_dialog = GeneratorSettingsDialog()
        self.bode_dialog = BodeDialog()
        self.impedance_dialog = ImpedanceDialog()

        # Slot and signal connections
        self.refresh.clicked.connect(self.on_refresh)
        self.connection.clicked.connect(self.on_connect)
        self.disconnection.clicked.connect(self.on_disconnect)
        self.oscilloscope_settings.clicked.connect(self.on_oscilloscope_settings)
        self.generator_settings.clicked.connect(self.on_generator_settings)
        self.measure_bode.clicked.connect(self.on_bode)
        self.measure_input_impedance.clicked.connect(self.on_impedance)

        self.go_device_connection()

    ##############################
    # General MainWindow Methods #
    ##############################
    def go_device_connection(self):
        self.stackedWidget.setCurrentIndex(self.widget_map["DEVICE_CONNECTION"])

    def go_main_menu(self):
        self.stackedWidget.setCurrentIndex(self.widget_map["MAIN_MENU"])

    ######################################
    # MainWindow Device Connection Slots #
    ######################################
    def on_refresh(self):
        """ Refreshing the oscilloscope and generator devices list """
        self.connected_devices = []
        self.oscilloscopes.clear()
        self.generators.clear()

        # Status flags
        excluded_devices = 0

        # Updating the oscilloscope and generator detected devices
        devices = LabTool.get_devices()
        for device in devices:
            device_info = LabTool.get_device_information(device)
            device_type = LabTool.is_device_detected(device_info)
            if device_type is InstrumentType.Generator or device_type is InstrumentType.Oscilloscope:
                self.connected_devices.append(
                    {
                        "device-id": device,
                        "device-type": device_type,
                        "device-brand": device_info["brand"],
                        "device-model": device_info["model"],
                        "device-series-number": device_info["series-number"],
                        "device-uid": "{} - {} - {}".format(
                            device_info["brand"],
                            device_info["model"],
                            device_info["series-number"]
                        )
                    }
                )
            else:
                excluded_devices += 1

        # Loading devices to the GUI List Widgets
        self.generators.addItems(
            [
                connected_device["device-uid"]
                for connected_device in self.connected_devices
                if connected_device["device-type"] is InstrumentType.Generator
            ]
        )

        self.oscilloscopes.addItems(
            [
                connected_device["device-uid"]
                for connected_device in self.connected_devices
                if connected_device["device-type"] is InstrumentType.Oscilloscope
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
        self.connection.setEnabled(len(self.oscilloscopes.currentText()) and len(self.generators.currentText()))

    def on_connect(self):
        self.oscilloscope = self.open_device_by_uid(self.oscilloscopes.currentText())
        self.generator = self.open_device_by_uid(self.generators.currentText())

        self.oscilloscope_used.setText(self.oscilloscopes.currentText())
        self.generator_used.setText(self.generators.currentText())

        self.go_main_menu()

    def open_device_by_uid(self, uid: str):
        for connected_device in self.connected_devices:
            if connected_device["device-uid"] == uid:
                return LabTool.open_device_by_id(connected_device["device-id"])

    ##############################
    # MainWindow Main Menu Slots #
    ##############################
    def on_disconnect(self):
        self.oscilloscope.close()
        self.generator.close()
        self.oscilloscope = self.generator = None
        self.go_device_connection()

    def on_oscilloscope_settings(self):
        self.oscilloscope_settings_dialog.exec()

    def on_generator_settings(self):
        self.generator_settings_dialog.exec()

    def on_bode(self):
        if self.bode_dialog.exec():
            algorithm = BodeAlgorithm(
                self.oscilloscope,
                self.generator,
                self.bode_dialog.make_requirements(),
                self.oscilloscope_settings_dialog.make_channel_setup(),
                self.oscilloscope_settings_dialog.make_trigger_setup(),
                self.oscilloscope_settings_dialog.make_acquire_setup(),
                self.oscilloscope_settings_dialog.make_timebase_setup(),
                self.generator_settings_dialog.make_generator_setup(),
                self.generator_settings_dialog.make_preferences_setup()
            )

            dialog = OutputDialog(algorithm)
            dialog.exec()

    def on_impedance(self):
        if self.impedance_dialog.exec():
            algorithm = ImpedanceAlgorithm(
                self.oscilloscope,
                self.generator,
                self.impedance_dialog.make_requirements(),
                self.oscilloscope_settings_dialog.make_channel_setup(),
                self.oscilloscope_settings_dialog.make_trigger_setup(),
                self.oscilloscope_settings_dialog.make_acquire_setup(),
                self.oscilloscope_settings_dialog.make_timebase_setup(),
                self.generator_settings_dialog.make_generator_setup(),
                self.generator_settings_dialog.make_preferences_setup()
            )

            dialog = OutputDialog(algorithm)
            dialog.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
