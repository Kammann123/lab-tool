# python native modules

# third-party modules
from PyQt5.QtWidgets import *

# labtool project modules
from app.designer.generator_settings.generator_settings import Ui_GeneratorSettings

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


class GeneratorSettingsDialog(QDialog, Ui_GeneratorSettings):

    def __init__(self, *args, **kwargs):
        super(GeneratorSettingsDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.code.setStyleSheet("color: rgba(0, 255, 0, 255);")

        # Dialog variables!
        self.changes_detected = False

        # Connecting slots and signals
        self.apply.clicked.connect(self.on_apply)
        self.ok.clicked.connect(self.on_ok)

        self.generator_vpp.valueChanged.connect(self.on_changes)
        self.establishment_time.valueChanged.connect(self.on_changes)
        self.start_frequency.valueChanged.connect(self.on_changes)
        self.stop_frequency.valueChanged.connect(self.on_changes)
        self.samples.valueChanged.connect(self.on_changes)
        self.scale.currentTextChanged.connect(self.on_changes)

        self.preferences_setup = {
            "delay": 0.01,
            "stable-time": float(self.establishment_time.value()),
            "scale": LabTool.to_enum(self.scale.currentText(), BodeScale),
            "start-frequency": float(self.start_frequency.value()),
            "stop-frequency": float(self.stop_frequency.value()),
            "samples": int(self.samples.value())
        }

        self.generator_setup = {
            "amplitude": float(self.generator_vpp.value())
        }

    ######################
    # GUI Dialog Outputs #
    ######################
    def make_preferences_setup(self) -> dict:
        """ Returns the setup object of the preferences """
        return self.preferences_setup

    def make_generator_setup(self) -> dict:
        """ Returns the setup object of the generator """
        return self.generator_setup

    ####################
    # GUI Dialog Slots #
    ####################
    def on_apply(self):
        """ Applies changes! """
        if self.changes_detected:
            self.changes_detected = False

            if self.start_frequency.value() < self.stop_frequency.value():
                self.preferences_setup = {
                    "delay": 0.01,
                    "stable-time": float(self.establishment_time.value()),
                    "scale": LabTool.to_enum(self.scale.currentText(), BodeScale),
                    "start-frequency": float(self.start_frequency.value()),
                    "stop-frequency": float(self.stop_frequency.value()),
                    "samples": int(self.samples.value())
                }

                self.generator_setup = {
                    "amplitude": float(self.generator_vpp.value())
                }

                self.code.setStyleSheet("color: rgba(0, 255, 0, 255);")
                self.status.setText("All changes have been saved.")
            else:
                self.status.setText("Start frequency is higher than the stop frequency...")

    def on_ok(self):
        """ Finishes the dialog process! """
        self.accept()

    def on_changes(self):
        """ Changes where detected on the GUI! """
        if not self.changes_detected:
            self.changes_detected = True
            self.code.setStyleSheet("color: rgba(255, 0, 0, 255);")
            self.status.setText("Changes detected! Please press Apply to save current settings.")


if __name__ == "__main__":
    app = QApplication([])
    dialog = GeneratorSettingsDialog()
    dialog.exec()
    print(dialog.make_generator_setup())
    print(dialog.make_preferences_setup())
    app.exec()
