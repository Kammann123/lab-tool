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
from labtool.base.instrument import Instrument


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


class TimebaseMode(Enum):
    Main = "Main"
    Delayed = "Delayed"
    XY = "XY"
    Roll = "Roll"


class TriggerMode(Enum):
    Edge = "Edge"


class TriggerSweep(Enum):
    Auto = "Auto"
    Normal = "Normal"


class TriggerSlope(Enum):
    Negative = "Negative"
    Positive = "Positive"
    Either = "Either"
    Alternate = "Alternate"


class Sources(Enum):
    Channel_1 = "Channel_1"
    Channel_2 = "Channel_2"
    Channel_3 = "Channel_3"
    Channel_4 = "Channel_4"
    External = "External"
    Line = "Line"


class WaveformFormat(Enum):
    Word = "WORD"
    Byte = "BYTE"
    Ascii = "ASCII"


###########################
# Oscilloscope Base Class #
###########################
class Oscilloscope(Instrument, ABC):
    """ Oscilloscope Base Class.
    When inheriting to define a child class, static parameters are needed
    to be recognized by the labtool """

    ###################
    # COMMON COMMANDS #
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
    def range(self, channel: int, range_value: float):
        """ Sets the range of the vertical axis of the channel """
        pass

    @abstractmethod
    def scale(self, channel: int, scale_value: float):
        """ Sets the vertical scale of the channel """
        pass

    @abstractmethod
    def display(self, channel: int, status: bool):
        """ Sets the Channel Status in the oscilloscope's display """
        pass

    @abstractmethod
    def offset(self, channel: int, offset_value: float):
        """ Sets the offset value of the channel in the display """
        pass

    #####################
    # TIMEBASE COMMANDS #
    #####################

    @abstractmethod
    def timebase_mode(self, mode: TimebaseMode):
        """ Sets the timebase mode of the oscilloscope """
        pass

    @abstractmethod
    def timebase_range(self, time_range: float):
        """ Sets the full range of the horizontal axis of the oscilloscope """
        pass

    @abstractmethod
    def timebase_scale(self, scale_value: float):
        """ Sets the scale value of the time base """
        pass

    ####################
    # TRIGGER COMMANDS #
    ####################

    @abstractmethod
    def trigger_mode(self, mode: TriggerMode):
        """ Setting the trigger mode of the oscilloscope """
        pass

    @abstractmethod
    def trigger_sweep(self, sweep: TriggerSweep):
        """ Setting the trigger sweep of the oscilloscope """
        pass

    @abstractmethod
    def trigger_edge_level(self, level_value: float):
        """ Setting the level of the edge triggering mode """
        pass

    @abstractmethod
    def trigger_edge_source(self, source: Sources):
        """ Setting the edge triggering source """
        pass

    @abstractmethod
    def trigger_edge_slope(self, slope: TriggerSlope):
        """ Setting the edge triggering slope """
        pass

    #####################
    # WAVEFORM COMMANDS #
    #####################

    @abstractmethod
    def waveform_source(self, source: Sources):
        """ Sets the source from which waveform data will be captured """
        pass

    @abstractmethod
    def waveform_unsigned(self, unsigned: bool):
        """ Sets whether byte packets are transferred as signed or unsigned """
        pass

    @abstractmethod
    def waveform_format(self, waveform_format: WaveformFormat):
        """ Sets the format of data being transferred from the waveform"""
        pass

    @abstractmethod
    def waveform_points(self, points: int):
        """ Sets the number of points to be taken from the waveform data """
        pass

    @abstractmethod
    def waveform_data(self):
        """ Returns the waveform data """
        pass

    @abstractmethod
    def waveform_preamble(self):
        """ Returns the waveform data preamble used to decode byte data """
        pass

    #####################
    # DIGITIZE COMMANDS #
    #####################

    @abstractmethod
    def digitize(self, source: Sources):
        """ Acquires the waveform of a selected channel using the current settings. """
        pass

    ####################
    # MEASURE COMMANDS #
    ####################

    @abstractmethod
    def measure_vpp(self, source: Sources):
        """ Measures the peak to peak voltage of the given source """
        pass

    @abstractmethod
    def measure_vratio(self, target_source: Sources, reference_source: Sources):
        """ Measures the voltage ratio between the target and the reference sources. """
        pass

    @abstractmethod
    def measure_phase(self, target_sources: Sources, reference_sources: Sources):
        """ Measures the phase of the target source """
        pass

    ###########################
    # SUBSYSTEM SETUP METHODS #
    ###########################

    def setup_acquire(self, setup: AcquireSetup):
        """ Sets up all the parameters of the acquire subsystem """
        if setup.mode is not None:
            self.acquire_mode(setup.mode)
        if setup.average_count is not None:
            self.acquire_average_count(setup.average_count)

    def setup_timebase(self, setup: TimebaseSetup):
        """ Sets up all the parameters of the timebase subsystem using a class
        which contains the parameters values. """
        if setup.mode is not None:
            self.timebase_mode(setup.mode)
        if setup.range is not None:
            self.timebase_range(setup.range)
        if setup.scale is not None:
            self.timebase_scale(setup.scale)

    def setup_trigger(self, setup: TriggerSetup):
        """ Sets up all the parameters of the trigger subsystem using a class
        which contains the parameter values. """
        if setup.mode is not None:
            self.trigger_mode(setup.mode)
        if setup.sweep is not None:
            self.trigger_sweep(setup.sweep)
        if setup.level is not None:
            self.trigger_edge_level(setup.level)
        if setup.source is not None:
            self.trigger_edge_source(setup.source)
        if setup.slope is not None:
            self.trigger_edge_slope(setup.slope)

    def setup_channel(self, channel: int, setup: ChannelSetup):
        """ Sets up all the parameters of a channel by one using a
        class containing the parameter values. """
        if setup.bandwidth_limit is not None:
            self.bandwidth_limit(channel, setup.bandwidth_limit)
        if setup.coupling is not None:
            self.coupling(channel, setup.coupling)
        if setup.probe is not None:
            self.probe(channel, setup.probe)
        if setup.range is not None:
            self.range(channel, setup.range)
        if setup.scale is not None:
            self.scale(channel, setup.scale)
        if setup.display is not None:
            self.display(channel, setup.display)
        if setup.offset is not None:
            self.offset(channel, setup.offset)


##############################
# Oscilloscope setup classes #
##############################

""" Note: If any of the parameters set in the Setup classes has a None value, then
    setting up that option in the oscilloscope channel will be omitted. """


class AcquireSetup(object):
    """ Acquire setup values """

    def __init__(self,
                 acquire_mode=None,
                 acquire_average_count=None):
        self.mode = acquire_mode
        self.average_count = acquire_average_count


class ChannelSetup(object):
    """ Channel setup values """

    def __init__(self,
                 bandwidth_limit=None,
                 coupling=None,
                 probe=None,
                 range_value=None,
                 scale=None,
                 display=None,
                 offset=None):
        self.bandwidth_limit = bandwidth_limit
        self.coupling = coupling
        self.probe = probe
        self.range = range_value
        self.scale = scale
        self.display = display
        self.offset = offset


class TriggerSetup(object):
    """ Trigger setup values """

    def __init__(self,
                 mode=None,
                 sweep=None,
                 level=None,
                 source=None,
                 slope=None):
        self.mode = mode
        self.sweep = sweep
        self.level = level
        self.source = source
        self.slope = slope


class TimebaseSetup(object):
    """ Timebase setup values """

    def __init__(self,
                 mode=None,
                 time_range=None,
                 time_scale=None):
        self.mode = mode
        self.range = time_range
        self.scale = time_scale
