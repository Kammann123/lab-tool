# python native modules
import sys

# third-party modules
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# labtool project modules
from app.designer.window.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
