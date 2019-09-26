# python native modules

# third-party modules
from PyQt5.Qt import *

# labtool project modules
from app.designer.output.output import Ui_Dialog


class OutputDialog(QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super(OutputDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # OutputDialog Members
        self.results = []
        self.result_fields = []

    ###########################
    # GUI Output Dialog Slots #
    ###########################
    def on_stop(self):
        """ Stops the measuring process """
        pass

    def on_excel(self):
        """ Exports the excel file """
        pass

    def on_plot(self):
        """ Open the plot dialog """
        pass

    ###############################
    # GUI Output Dialog Interface #
    ###############################
    def set_status(self, status: str):
        """ Sets the status message on the Output Dialog """
        self.status.setText(status)

    def set_progress(self, progress: int):
        """ Sets the current progress value on the Output Dialog """
        self.progress.setValue(progress)

    def set_results(self, results: list):
        """ Sets the list of samples defined as dictionaries """
        # Save current result values
        self.results = results
        self.result_fields = self.results[0].keys()

        # Set the sample field of the GUI
        self.samples.setValue(len(self.results))

        # Set the fields of the GUI
        self.fields.clear()
        self.fields.addItems(self.result_fields)

        # Enables the buttons
        self.excel.setEnabled(True)
        self.plot.setEnabled(True)


if __name__ == "__main__":
    app = QApplication([])
    dialog = OutputDialog()
    dialog.exec()
    app.exec()
