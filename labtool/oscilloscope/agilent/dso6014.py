"""
DSO6014 Agilent Model class implementation.
"""

# labtool project modules
from labtool.oscilloscope.base.oscilloscope import Oscilloscope
from labtool.oscilloscope.base.oscilloscope import AcquireMode


######################
# Agilent Exceptions #
######################

class AverageCountError(Exception):
    def __init__(self):
        super(AverageCountError, self).__init__(
            "Average count value entered was not valid, remember using a power of 2"
        )


#######################
# Agilent model class #
#######################
class AgilentDSO6014(Oscilloscope):
    """ Agilent DSO6014 Oscilloscope model """

    # Instrument information
    brand = "AGILENT"
    model = "DSO6014"

    # Internal dictionaries of agilent syntax
    acquire_modes = {
        AcquireMode.Normal: "NORMal",
        AcquireMode.Average: "AVERage",
        AcquireMode.HighResolution: "HRESolution",
        AcquireMode.PeakDetect: "PEAK"
    }

    ###################
    # COMMON COMMANDS
    ###################

    def reset(self):
        """ Resets the oscilloscope. """
        self.resource.write("*RST")

    def clear(self):
        """ Clears the oscilloscope's status registers. """
        self.resource.write("*CLS")

    def who(self) -> str:
        """ Returns a string with an oscilloscope's identifier. """
        return self.resource.query("*IDN?")

    #################
    # ROOT COMMANDS #
    #################

    def autoscale(self):
        """ Autoscaling the oscilloscope's channels. """
        self.resource.write(":AUToscale")

    def run(self):
        """ Runs the measuring process of the oscilloscope. """
        self.resource.write(":RUN")

    def stop(self):
        """ Stops the oscilloscope measuring, freezing the signal waveform
        that had been captured in the screen. """
        self.resource.write(":STOP")

    ####################
    # ACQUIRE COMMANDS #
    ####################

    def acquire_mode(self, mode: AcquireMode):
        """ Sets the AcquireMode of the oscilloscope """
        self.resource.write(":ACQuire:TYPE {}".format(acquire_modes[mode]))

    def acquire_average_count(self, count: int):
        """ Sets the amount of samples to be used when averaging the signal. """
        if type(count) != int:
            raise ValueError("Integer value expected for the average count.")

        if is_power_of(count, 2):
            self.resource.write(":ACQuire:COUNt {}".format(count))
        else:
            raise AverageCountError


#############
# Functions #
#############

def is_power_of(target: int, power: int) -> bool:
    """ Verifies if a number is a power of another number """
    if target != 0:

        auxiliar = target
        while auxiliar != 1:
            if auxiliar % power:
                return False
            auxiliar /= power

        return True
    else:
        return False
