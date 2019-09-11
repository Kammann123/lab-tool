"""
Oscilloscope base class. It contains the base methods that should be defined
or implemented by any child class defining a specific oscilloscope model.

Note: Lucas does not like this, but the easiest program structure will be used.

Note: No idea if all oscilloscopes from the same brand use the same standard,
sounds the most logic thing, but there could be differences in features...
"""

# python native modules
from abc import ABC
from abc import abstractmethod

from enum import Enum


# labtool project modules
from labtool.instrument import Instrument


########################################
# Oscilloscope Enumeration Definitions #
########################################
class AcquireMode(Enum):
    Normal = "Normal"
    Average = "Average"
    HighResolution = "HighResolution"
    PeakDetect = "PeakDetect"


class BandwidthLimit(Enum):
    OFF = "OFF"
    ON = "ON"


class Coupling(Enum):
    AC = "AC"
    DC = "DC"


class Display(Enum):
    ON = "ON"
    OFF = "OFF"


###########################
# Oscilloscope Base Class #
###########################
class Oscilloscope(Instrument, ABC):
    """ Oscilloscope Base Class.
    When inheriting to define a child class, static parameters are needed
    to be recognized by the labtool """

    ###################
    # COMMON COMMANDS
    ###################

    @abstractmethod
    def reset(self):
        """ Resets the oscilloscope. """
        pass

    @abstractmethod
    def clear(self):
        """ Clears the oscilloscope's status registers. """
        pass

    @abstractmethod
    def who(self) -> str:
        """ Returns a string with an oscilloscope's identifier. """
        pass

    #################
    # ROOT COMMANDS #
    #################

    @abstractmethod
    def autoscale(self):
        """ Autoscaling the oscilloscope's channels. """
        pass

    @abstractmethod
    def run(self):
        """ Runs the measuring process of the oscilloscope. """
        pass

    @abstractmethod
    def stop(self):
        """ Stops the oscilloscope measuring, freezing the signal waveform
        that had been captured in the screen. """
        pass

    ####################
    # ACQUIRE COMMANDS #
    ####################

    @abstractmethod
    def acquire_mode(self, mode: AcquireMode):
        """ Sets the AcquireMode of the oscilloscope """
        pass

    @abstractmethod
    def acquire_average_count(self, count: int):
        """ Sets the amount of samples to be used when averaging the signal. """
        pass

    ####################
    # CHANNEL COMMANDS #
    ####################

    @abstractmethod
    def bandwidth_limit(self, channel: int, status: BandwidthLimit):
        """ Sets the status of the BandwidthLimit """
        pass

    @abstractmethod
    def coupling(self, channel: int, status: Coupling):
        """ Sets the status of the Coupling """
        pass

    @abstractmethod
    def probe(self, channel: int, probe_value: int):
        """ Sets the probe value of the channel """
        pass

    @abstractmethod
    def scale(self, channel: int, scale_value: float):
        """ Sets the vertical scale of the channel """
        pass

    @abstractmethod
    def display(self, channel: int, status: Display):
        """ Sets the Channel Status in the oscilloscope's display """
        pass

    @abstractmethod
    def offset(self, channel: int, offset_value: float):
        """ Sets the offset value of the channel in the display """
        pass
