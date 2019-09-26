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
from labtool.base.instrument import InstrumentType


########################################
# Oscilloscope Enumeration Definitions #
########################################
class AcquireMode(Enum):
    Normal = "Normal"
    Average = "Average"
    HighResolution = "HighResolution"
    PeakDetect = "PeakDetect"


class BandwidthLimit(Enum):
    On = "On"
    Off = "Off"


class ChannelStatus(Enum):
    On = "On"
    Off = "Off"


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
    Channel_1 = "Channel 1"
    Channel_2 = "Channel 2"
    Channel_3 = "Channel 3"
    Channel_4 = "Channel 4"
    Channel_5 = "Channel 5"
    Channel_6 = "Channel 6"
    External = "External"
    Math = "Math"
    Function = "Function"
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

    # Oscilloscope information
    type = InstrumentType.Oscilloscope

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
    def set_acquire_mode(self, mode: AcquireMode):
        """ Sets the AcquireMode of the oscilloscope """
        pass

    @abstractmethod
    def set_acquire_average_count(self, count: int):
        """ Sets the amount of samples to be used when averaging the signal. """
        pass

    ####################
    # CHANNEL COMMANDS #
    ####################

    @abstractmethod
    def set_bandwidth_limit(self, channel: int, status: bool):
        """ Sets the status of the BandwidthLimit """
        pass

    @abstractmethod
    def set_coupling(self, channel: int, status: Coupling):
        """ Sets the status of the Coupling """
        pass

    @abstractmethod
    def set_probe(self, channel: int, probe_value: int):
        """ Sets the probe value of the channel """
        pass

    @abstractmethod
    def set_range(self, channel: int, range_value: float):
        """ Sets the range of the vertical axis of the channel """
        pass

    @abstractmethod
    def get_range(self, channel: int) -> float:
        """ Returns the range setting of the given channel """
        pass

    @abstractmethod
    def set_scale(self, channel: int, scale_value: float):
        """ Sets the vertical scale of the channel """
        pass

    @abstractmethod
    def set_display(self, channel: int, status: bool):
        """ Sets the Channel Status in the oscilloscope's display """
        pass

    @abstractmethod
    def set_offset(self, channel: int, offset_value: float):
        """ Sets the offset value of the channel in the display """
        pass

    #####################
    # TIMEBASE COMMANDS #
    #####################

    @abstractmethod
    def set_timebase_mode(self, mode: TimebaseMode):
        """ Sets the timebase mode of the oscilloscope """
        pass

    @abstractmethod
    def set_timebase_range(self, time_range: float):
        """ Sets the full range of the horizontal axis of the oscilloscope """
        pass

    @abstractmethod
    def set_timebase_scale(self, scale_value: float):
        """ Sets the scale value of the time base """
        pass

    ####################
    # TRIGGER COMMANDS #
    ####################

    @abstractmethod
    def set_trigger_mode(self, mode: TriggerMode):
        """ Setting the trigger mode of the oscilloscope """
        pass

    @abstractmethod
    def set_trigger_sweep(self, sweep: TriggerSweep):
        """ Setting the trigger sweep of the oscilloscope """
        pass

    @abstractmethod
    def set_trigger_edge_level(self, level_value: float):
        """ Setting the level of the edge triggering mode """
        pass

    @abstractmethod
    def set_trigger_edge_source(self, source: Sources):
        """ Setting the edge triggering source """
        pass

    @abstractmethod
    def set_trigger_edge_slope(self, slope: TriggerSlope):
        """ Setting the edge triggering slope """
        pass

    @abstractmethod
    def set_hf_reject(self, value: bool):
        """ Setting the HFReject """
        pass

    @abstractmethod
    def set_n_reject(self, value: bool):
        """ Setting the NFReject """
        pass

    #####################
    # WAVEFORM COMMANDS #
    #####################

    @abstractmethod
    def set_waveform_source(self, source: Sources):
        """ Sets the source from which waveform data will be captured """
        pass

    @abstractmethod
    def set_waveform_unsigned(self, unsigned: bool):
        """ Sets whether byte packets are transferred as signed or unsigned """
        pass

    @abstractmethod
    def set_waveform_format(self, waveform_format: WaveformFormat):
        """ Sets the format of data being transferred from the waveform"""
        pass

    @abstractmethod
    def set_waveform_points(self, points: int):
        """ Sets the number of points to be taken from the waveform data """
        pass

    @abstractmethod
    def set_waveform_data(self):
        """ Returns the waveform data """
        pass

    @abstractmethod
    def set_waveform_preamble(self):
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
    def measure_vmax(self, source: Sources):
        """ Measures the vmax voltage of the given source """
        pass

    @abstractmethod
    def measure_vmin(self, source: Sources):
        """ Measures the vmin voltage of the given source """
        pass

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

    ##################
    # HELPER METHODS #
    ##################

    @staticmethod
    def source_to_channel(source: Sources):
        """ Returns the channel number when receiving the Source Enum data type """
        if source.value[:-1] == "Channel ":
            return int(source.value[-1])
        return None

    @staticmethod
    def channel_to_source(number: int):
        """ Returns the source enum definition from the channel number """
        formatted_channel = "Channel {}".format(number)
        for source in Sources:
            if source.value == formatted_channel:
                return source
        return None

    ###########################
    # SUBSYSTEM SETUP METHODS #
    ###########################

    def setup_acquire(self, **kwargs):
        """ Sets up all the parameters of the acquire subsystem.
            [Options]
                + acquire-mode: The AcquireMode used for the oscilloscope.
                + average-count: The number of sameples used to averaging the signal shown in the screen.
                """
        if "acquire-mode" in kwargs.keys():
            self.set_acquire_mode(kwargs["acquire-mode"])
        if "average-count" in kwargs.keys():
            self.set_acquire_average_count(kwargs["average-count"])

    def setup_timebase(self, **kwargs):
        """ Sets up all the parameters of the timebase subsystem using a class
        which contains the parameters values.
            [Options]
                + timebase-mode: The TimebaseMode used for the oscilloscope.
                + timebase-range: Sets the range of the timebase.
                + timebase-scale: Sets the scale of the timebase.
                """
        if "timebase-mode" in kwargs.keys():
            self.set_timebase_mode(kwargs["timebase-mode"])
        if "timebase-range" in kwargs.keys():
            self.set_timebase_range(kwargs["timebase-range"])
        if "timebase-scale" in kwargs.keys():
            self.set_timebase_scale(kwargs["timebase-scale"])

    def setup_trigger(self, **kwargs):
        """ Sets up all the parameters of the trigger subsystem using a class
        which contains the parameter values.
            [Options]
                + trigger-mode: TriggerMode
                + trigger-sweep: TriggerSweep
                + trigger-edge-level: Level value
                + trigger-edge-source: Source
                + trigger-edge-slope: TriggerSlope
                """
        if "trigger-mode" in kwargs.keys():
            self.set_trigger_mode(kwargs["trigger-mode"])
        if "trigger-sweep" in kwargs.keys():
            self.set_trigger_sweep(kwargs["trigger-sweep"])
        if "trigger-edge-level" in kwargs.keys():
            self.set_trigger_edge_level(kwargs["trigger-edge-level"])
        if "trigger-edge-source" in kwargs.keys():
            self.set_trigger_edge_source(kwargs["trigger-edge-source"])
        if "trigger-edge-slope" in kwargs.keys():
            self.set_trigger_edge_slope(kwargs["trigger-edge-slope"])
        if "n-reject" in kwargs.keys():
            self.set_n_reject(kwargs["n-reject"])
        if "hf-reject" in kwargs.keys():
            self.set_hf_reject(kwargs["hf-reject"])

    def setup_channel(self, channel: int, **kwargs):
        """ Sets up all the parameters of a channel by one using a
        class containing the parameter values.
            [Options]
                + bandwidth_limit: BandwidthLimit
                + coupling: Coupling
                + probe: Probe
                + range: Range value
                + scale: Scale value
                + display: Boolean value if should be displayed
                + offset: Offset value
                """
        if "bandwidth_limit" in kwargs.keys():
            self.set_bandwidth_limit(channel, kwargs["bandwidth_limit"])
        if "coupling" in kwargs.keys():
            self.set_coupling(channel, kwargs["coupling"])
        if "probe" in kwargs.keys():
            self.set_probe(channel, kwargs["probe"])
        if "range" in kwargs.keys():
            self.set_range(channel, kwargs["range"])
        if "scale" in kwargs.keys():
            self.set_scale(channel, kwargs["scale"])
        if "display" in kwargs.keys():
            self.set_display(channel, kwargs["display"])
        if "offset" in kwargs.keys():
            self.set_offset(channel, kwargs["offset"])
