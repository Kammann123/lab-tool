# python native modules

# third-party modules
from PyQt5.QtWidgets import *

# labtool project modules
from app.designer.bode.bode import Ui_Dialog

from labtool.oscilloscope.base.oscilloscope import Sources
from labtool.tool import LabTool


class BodeDialog(QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super(BodeDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Signal and slot connections
        self.input_channel.currentTextChanged.connect(self.on_changes)
        self.output_channel.currentTextChanged.connect(self.on_changes)
        self.ok.clicked.connect(self.on_ok)

        self.on_changes()

    def make_requirements(self) -> dict:
        """ Returns a dictionary with Requirements data to run a bode measurement algorithm """
        return {
            "input-channel": LabTool.to_enum("Channel {}".format(self.input_channel.currentText()), Sources),
            "output-channel": LabTool.to_enum("Channel {}".format(self.output_channel.currentText()), Sources)
        }

    def on_changes(self):
        """ Detects changes done in the Bode settings and verifies if Ok can be clicked! """
        self.ok.setEnabled(self.input_channel.currentText() != self.output_channel.currentText())

    def on_ok(self):
        """ Verifies if settings are valid and accepts the bode request """
        self.accept()


if __name__ == "__main__":
    app = QApplication([])
    dialog = BodeDialog()
    dialog.exec()
    app.exec()
