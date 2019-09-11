"""
DSO6014 Agilent Model class implementation.
"""

# labtool project modules
from labtool.oscilloscope.base.oscilloscope import Oscilloscope
from labtool.oscilloscope.base.oscilloscope import AcquireMode
from labtool.oscilloscope.base.oscilloscope import BandwidthLimit
from labtool.oscilloscope.base.oscilloscope import Coupling
from labtool.oscilloscope.base.oscilloscope import Display


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

    bandwidth_limits = {
        BandwidthLimit.ON: "1",
        BandwidthLimit.OFF: "0"
    }

    display_status = {
        Display.ON: "1",
        Display.OFF: "0"
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
        self.resource.write(":ACQuire:TYPE {}".format(self.acquire_modes[mode]))

    def acquire_average_count(self, count: int):
        """ Sets the amount of samples to be used when averaging the signal. """
        if type(count) != int:
            raise ValueError("Integer value expected for the average count.")

        if is_power_of(count, 2):
            self.resource.write(":ACQuire:COUNt {}".format(count))
        else:
            raise AverageCountError

    ####################
    # CHANNEL COMMANDS #
    ####################

    def bandwidth_limit(self, channel: int, status: BandwidthLimit):
        """ Sets the status of the BandwidthLimit """
        self.resource.write(":CHAN{}:BWL {}".format(channel, self.bandwidth_limits[status]))

    def coupling(self, channel: int, status: Coupling):
        """ Sets the status of the Coupling """
        self.resource.write(":CHAN{}:COUP {}".format(channel, status.value))

    def probe(self, channel: int, probe_value: int):
        """ Sets the probe value of the channel """
        self.resource.write(":CHAN{}:PROB {}".format(channel, probe_value))

    def scale(self, channel: int, scale_value: float):
        """ Sets the vertical scale of the channel """
        self.resource.write(":CHAN{}:SCAL {}".format(channel, scale_value))

    def display(self, channel: int, status: Display):
        """ Sets the Channel Status in the oscilloscope's display """
        self.resource.write(":CHAN{}:DISP {}".format(channel, self.display_status[status]))

    def offset(self, channel: int, offset_value: float):
        """ Sets the offset value of the channel in the display """
        self.resource.write(":CHAN{}:OFFS {}".format(channel, offset_value))


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
