"""
Generator base class. It contains the base methods that should be defined
or implemented by any child class defining a specific generator model.

Note: Neither Charlie Nor Lucas like this, but the easiest program structure will be used.

Note: No idea if all generators from the same brand use the same standard,
sounds like the most logic thing, but there could be differences in features...
"""

# python native modules
from abc import ABC
from abc import abstractmethod

from enum import Enum

# labtool project modules
from labtool.base.instrument import Instrument
from labtool.base.instrument import InstrumentType


#####################################
# Generator Enumeration Definitions #
#####################################

class Waveform(Enum):
    Sine = "Sine"
    Square = "Square"
    Ramp = "Ramp"


class OutputMode(Enum):
    OFF = "OFF"
    ON = "ON"


class SyncMode(Enum):
    OFF = "OFF"
    ON = "ON"


class OutputPolarity(Enum):
    Normal = "Normal"
    Inverted = "Inverted"


class OutputLoad(Enum):
    Value = "Value"
    HighZ = "HighZ"


###########################
# Generator Base Class    #
###########################

class Generator(Instrument, ABC):
    """ Generator Base Class.
    When inheriting to define a child class, static parameters are needed
    to be recognized by the labtool """

    # Generator information
    type = InstrumentType.Generator

    ###################
    # COMMON COMMANDS #
    ###################

    @abstractmethod
    def reset(self):
        """ Resets the generator. """
        pass

    @abstractmethod
    def clear(self):
        """ Clears the generator's status registers. """
        pass

    @abstractmethod
    def who(self) -> str:
        """ Returns a string with an generator's identifier. """
        pass

    ##################
    # APPLY COMMANDS #
    ##################
    @abstractmethod
    def generate_signal(self, **kwargs):
        """ Generates a signal controlled by received parameters
            [Options]
                + waveform: Waveform
                + frequency: Frequency value
                + amplitude: Amplitude value
                + offset: Offset value
                """
        pass

    ############################
    # OUTPUT CONFIG COMMANDS   #
    ############################

    @abstractmethod
    def set_waveform(self, waveform: Waveform):
        """ Changes output waveform type, selectable from the ones in Enum """
        pass

    @abstractmethod
    def set_frequency(self, frequency: float):
        """ Changes output frequency """
        pass

    @abstractmethod
    def set_amplitude(self, amplitude: float):
        """ Changes output amplitude """
        pass

    @abstractmethod
    def set_offset(self, offset: float):
        """ Changes output offset """
        pass

    @abstractmethod
    def set_square_duty(self, percent: float):
        """ Changes output duty cycle, only applicable if output is Square """
        pass

    @abstractmethod
    def set_ramp_symmetry(self, percent: float):
        """ Changes output symmetry, only applicable if output is Ramp """
        pass

    @abstractmethod
    def set_output_mode(self, mode: OutputMode):
        """ Turns the output on or off depending on the arg """
        pass

    @abstractmethod
    def check_output_mode(self) -> OutputMode:
        """ Returns a OutputMode indicating output state """
        pass

    @abstractmethod
    def set_output_pol(self, polarity: OutputPolarity):
        """ Changes output polarity """
        pass

    @abstractmethod
    def check_output_polarity(self) -> OutputPolarity:
        """ Returns a OutputPolarity indicating output polarity """
        pass

    @abstractmethod
    def set_output_load(self, load: float, load_param: OutputLoad):
        """ Changes output load. It can be a fixed value or HighZ """
        pass

    @abstractmethod
    def check_output_load(self) -> (float, OutputLoad):
        """ Returns a tuple including a value and OutputLoad, if OutputLoad == OutputLoad.HighZ
            value contents have no sense """
        pass

    @abstractmethod
    def set_sync_mode(self, mode: SyncMode):
        """ Turns the Sync output on or off depending on the arg """
        pass

    @abstractmethod
    def check_sync_mode(self) -> SyncMode:
        """ Returns a OutputMode indicating output state """
        pass
