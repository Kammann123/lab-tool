"""
LabTool Graphic User-Interface (GUI) application
"""

# python native modules
import sys

# third-party modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

# labtool project modules
from app.designer.window import Ui_LabToolWindow


# Loading new available devices to use as Instruments...
from labtool.oscilloscope.agilent.agilent_dso6014 import AgilentDSO6014

from labtool.generator.agilent.agilent_33220a import Agilent33220A


class LabToolWindow(QMainWindow, Ui_LabToolWindow):

    def __init__(self, *args, **kwargs):
        super(LabToolWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LabToolWindow()
    window.show()
    sys.exit(app.exec())
