# python native modules

# third-party modules
from PyQt5.QtWidgets import *

# labtool project modules
from app.designer.oscilloscope_settings.oscilloscope_settings import Ui_OscSettings

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
from labtool.oscilloscope.base.oscilloscope import BandwidthLimit
from labtool.oscilloscope.base.oscilloscope import ChannelStatus


# noinspection PyMethodMayBeStatic
class OscilloscopeSettingsDialog(QDialog, Ui_OscSettings):

    def __init__(self, *args, **kwargs):
        super(OscilloscopeSettingsDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.code.setStyleSheet("color: rgba(0, 255, 0, 255);")

        # Dialog variables!
        self.changes_detected = False

        # Connecting slots and signals
        self.apply.clicked.connect(self.on_apply)
        self.ok.clicked.connect(self.on_ok)

        self.trigger_n_reject.toggled.connect(self.on_changes)
        self.trigger_hf_reject.toggled.connect(self.on_changes)
        self.trigger_level.valueChanged.connect(self.on_changes)
        self.trigger_sweep.currentTextChanged.connect(self.on_changes)
        self.trigger_slope.currentTextChanged.connect(self.on_changes)
        self.trigger_source.currentTextChanged.connect(self.on_changes)
        self.bw.toggled.connect(self.on_changes)
        self.coupling.currentTextChanged.connect(self.on_changes)
        self.probe.currentTextChanged.connect(self.on_changes)

    ######################
    # GUI Dialog Outputs #
    ######################
    def make_channel_setup(self) -> dict:
        """ Makes the setup object of a Channel """
        return {
            "bandwidth_limit": BandwidthLimit.On if self.bw.isChecked() else BandwidthLimit.Off,
            "coupling": LabTool.to_enum(self.coupling.currentText(), Coupling),
            "probe": int(self.probe.currentText()),
            "display": ChannelStatus.On,
            "range": 20,
            "offset": 0
        }

    def make_trigger_setup(self) -> dict:
        """ Makes the setup object of the Trigger """
        return {
            "trigger-mode": TriggerMode.Edge,
            "trigger-sweep": LabTool.to_enum(self.trigger_sweep.currentText(), TriggerSweep),
            "trigger-edge-level": float(self.trigger_level.value()),
            "trigger-edge-slope": LabTool.to_enum(self.trigger_slope.currentText(), TriggerSlope),
            "trigger-edge-source": LabTool.to_enum(self.trigger_source.currentText(), Sources),
            "hf-reject": self.trigger_hf_reject.isChecked(),
            "n-reject": self.trigger_n_reject.isChecked()
        }

    def make_acquire_setup(self) -> dict:
        """ Makes the setup object of the Acquire """
        return {
            "acquire-mode": AcquireMode.Average,
            "average-count": 2
        }

    def make_timebase_setup(self) -> dict:
        """ Makes the setup object of the Timebase """
        return {
            "timebase-mode": TimebaseMode.Main
        }

    ####################
    # GUI Dialog Slots #
    ####################
    def on_apply(self):
        """ Applies changes! """
        if self.changes_detected:
            self.changes_detected = False
            self.code.setStyleSheet("color: rgba(0, 255, 0, 255);")
            self.status.setText("All changes have been saved.")

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
    dialog = OscilloscopeSettingsDialog()
    dialog.exec()
    print(dialog.make_acquire_setup())
    print(dialog.make_channel_setup())
    print(dialog.make_timebase_setup())
    print(dialog.make_timebase_setup())
    app.exec()
