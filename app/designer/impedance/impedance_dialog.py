# python native modules

# third-party modules
from PyQt5.QtWidgets import *

# labtool project modules
from app.designer.impedance.impedance import Ui_Dialog

from labtool.oscilloscope.base.oscilloscope import Sources
from labtool.tool import LabTool


class ImpedanceDialog(QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super(ImpedanceDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.input_channel.currentTextChanged.connect(self.on_changes)
        self.generator_channel.currentTextChanged.connect(self.on_changes)
        self.ok.clicked.connect(self.on_ok)

        self.on_changes()

    def make_requirements(self) -> dict:
        """ Returns a dictionary with Requirements data to run a bode measurement algorithm """
        return {
            "resistance": self.resistance.value(),
            "input-channel": LabTool.to_enum("Channel {}".format(self.input_channel.currentText()), Sources),
            "generator-channel": LabTool.to_enum("Channel {}".format(self.generator_channel.currentText()), Sources)
        }

    def on_changes(self):
        """ Detects changes done in the Bode settings and verifies if Ok can be clicked! """
        self.ok.setEnabled(self.generator_channel.currentText() != self.input_channel.currentText())

    def on_ok(self):
        """ Verifies if settings are valid and accepts the bode request """
        self.accept()


if __name__ == "__main__":
    app = QApplication([])
    dialog = ImpedanceDialog()
    dialog.exec()
    print(dialog.make_requirements())
    app.exec()
