"""
LabTool module with a list of the available devices
"""


class LabTool(object):
    """ LabTool available devices """

    # Available devices in the LabTool
    available_oscilloscopes = []
    available_generators = []

    @staticmethod
    def add_oscilloscope(oscilloscope):
        """ Registers a new Oscilloscope Class """
        available_oscilloscopes.append(oscilloscope)

    @staticmethod
    def add_generator(generator):
        """ Registers a new Generator Class """
        available_generators.append(generator)
