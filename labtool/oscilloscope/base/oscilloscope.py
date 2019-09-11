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
