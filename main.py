# python native modules
import sys

# third-party modules
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# labtool project modules
from app.labtool_window import LabToolWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LabToolWindow()
    window.show()
    sys.exit(app.exec())
