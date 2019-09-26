# python native modules

# third-party modules
from PyQt5.QtWidgets import *

# labtool project modules
from app.designer.window.window import Ui_LabToolWindow


class MainWindow(QMainWindow, Ui_LabToolWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("LabTool")




if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
