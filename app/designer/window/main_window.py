# python native modules

# third-party modules
from PyQt5.QtWidgets import *

# labtool project modules
from app.designer.window.window import Ui_LabToolWindow
from app.designer.oscilloscope_settings.oscilloscope_settings_dialog import OscilloscopeSettingsDialog
from app.designer.generator_settings.generator_settings_dialog import GeneratorSettingsDialog

from labtool.base.instrument import InstrumentType
from labtool.tool import LabTool


class MainWindow(QMainWindow, Ui_LabToolWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("LabTool")

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

        # Slot and signal connections
        self.refresh.clicked.connect(self.on_refresh)
        self.connection.clicked.connect(self.on_connect)
        self.disconnection.clicked.connect(self.on_disconnect)
        self.oscilloscope_settings.clicked.connect(self.on_oscilloscope_settings)
        self.generator_settings.clicked.connect(self.on_generator_settings)

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
                if connected_device["device_type"] is InstrumentType.Generator
            ]
        )

        self.oscilloscopes.addItems(
            [
                connected_device["device-uid"]
                for connected_device in self.connected_devices
                if connected_device["device_type"] is InstrumentType.Oscilloscope
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

    def on_connect(self):
        self.oscilloscope = self.open_device_by_uid(self.oscilloscopes.currentText())
        self.generator = self.open_device_by_uid(self.generators.currentText())
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


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
