"""
DSO6014 Agilent Model class implementation.
"""

# labtool project modules
from labtool.oscilloscope.base.oscilloscope import Oscilloscope


class AgilentDSO6014(Oscilloscope):
    """ Agilent DSO6014 Oscilloscope model """

    # Instrument information
    brand = "AGILENT"
    model = "DSO6014"

    ###################
    # COMMON COMMANDS
    ###################

    def reset(self):
        """ Resets the oscilloscope. """
        self.

    def clear(self):
        """ Clears the oscilloscope's status registers. """
        pass

    def who(self) -> str:
        """ Returns a string with an oscilloscope's identifier. """
        pass

