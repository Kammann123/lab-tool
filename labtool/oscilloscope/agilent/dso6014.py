"""
DSO6014 Agilent Model class implementation.
"""

# labtool project modules
from labtool.oscilloscope.base.oscilloscope import Oscilloscope
from labtool.oscilloscope.base.oscilloscope import AcquireMode
from labtool.oscilloscope.base.oscilloscope import BandwidthLimit
from labtool.oscilloscope.base.oscilloscope import Coupling
from labtool.oscilloscope.base.oscilloscope import Display
from labtool.oscilloscope.base.oscilloscope import TimebaseMode
from labtool.oscilloscope.base.oscilloscope import TriggerMode
from labtool.oscilloscope.base.oscilloscope import Sources
from labtool.oscilloscope.base.oscilloscope import TriggerSlope
from labtool.oscilloscope.base.oscilloscope import TriggerSweep
from labtool.oscilloscope.base.oscilloscope import WaveformFormat

from labtool.tool import LabTool


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
    sources = {
        Sources.Channel_1: "CHANnel1",
        Sources.Channel_2: "CHANnel2",
        Sources.Channel_3: "CHANnel3",
        Sources.Channel_4: "CHANnel4",
        Sources.External: "EXTernal",
        Sources.Line: "LINE"
    }

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

    timebase_modes = {
        TimebaseMode.Main: "MAIN",
        TimebaseMode.Delayed: "WINDow",
        TimebaseMode.XY: "XY",
        TimebaseMode.Roll: "ROLL"
    }

    trigger_modes = {
        TriggerMode.Edge: "EDGE"
    }

    trigger_slopes = {
        TriggerSlope.Negative: "NEGative",
        TriggerSlope.Positive: "POSitive",
        TriggerSlope.Either: "EITHer",
        TriggerSlope.Alternate: "ALTernate"
    }

    trigger_sweeps = {
        TriggerSweep.Auto: "AUTO",
        TriggerSweep.Normal: "NORMal"
    }

    waveform_formats = {
        WaveformFormat.Word: "WORD",
        WaveformFormat.Byte: "BYTE",
        WaveformFormat.Ascii: "ASCii"
    }

    ###################
    # COMMON COMMANDS #
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

    def range(self, channel: int, range_value: float):
        """ Sets the range of the vertical axis of the channel """
        self.resource.write(":CHAN{}:RANG {}".format(channel, range_value))

    def scale(self, channel: int, scale_value: float):
        """ Sets the vertical scale of the channel """
        self.resource.write(":CHAN{}:SCAL {}".format(channel, scale_value))

    def display(self, channel: int, status: bool):
        """ Sets the Channel Status in the oscilloscope's display """
        self.resource.write(
            ":CHAN{}:DISP {}".format(
                channel,
                "1" if status else "0"
            )
        )

    def offset(self, channel: int, offset_value: float):
        """ Sets the offset value of the channel in the display """
        self.resource.write(":CHAN{}:OFFS {}".format(channel, offset_value))

    #####################
    # TIMEBASE COMMANDS #
    #####################

    def timebase_mode(self, mode: TimebaseMode):
        """ Sets the timebase mode of the oscilloscope """
        self.resource.write(":TIMebase:MODE {}".format(self.timebase_modes[mode]))

    def timebase_range(self, time_range: float):
        """ Sets the full range of the horizontal axis of the oscilloscope """
        self.resource.write(":TIMebase:RANGe {}".format(time_range))

    def timebase_scale(self, scale_value: float):
        """ Sets the scale value of the time base """
        self.resource.write(":TIMebase:SCALe {}".format(scale_value))

    ####################
    # TRIGGER COMMANDS #
    ####################

    def trigger_mode(self, mode: TriggerMode):
        """ Setting the trigger mode of the oscilloscope """
        self.resource.write(":TRIG:MODE {}".format(self.trigger_modes[mode]))

    def trigger_sweep(self, sweep: TriggerSweep):
        """ Setting the trigger sweep of the oscilloscope """
        self.resource.write(":TRIG:SWE {}".format(self.trigger_sweeps[sweep]))

    def trigger_edge_level(self, level_value: float):
        """ Setting the level of the edge triggering mode """
        self.resource.write(":TRIG[:EDGE]:LEV {}".format(level_value))

    def trigger_edge_source(self, source: Sources):
        """ Setting the edge triggering source """
        self.resource.write(":TRIG[:EDGE]:SOUR {}".format(self.sources[source]))

    def trigger_edge_slope(self, slope: TriggerSlope):
        """ Setting the edge triggering slope """
        self.resource.write(":TRIG[:EDGE]:SLOP {}".format(self.trigger_slopes[slopes]))

    #####################
    # WAVEFORM COMMANDS #
    #####################

    def waveform_source(self, source: Sources):
        """ Sets the source from which waveform data will be captured """
        self.resource.write(":WAV:SOUR {}".format(self.sources[source]))

    def waveform_unsigned(self, unsigned: bool):
        """ Sets whether byte packets are transferred as signed or unsigned """
        self.resource.write(
            ":WAV:UNS {}".format(
                "ON" if unsigned else "OFF"
            )
        )

    def waveform_format(self, waveform_format: WaveformFormat):
        """ Sets the format of data being transferred from the waveform"""
        self.resource.write(":WAV:FORM {}".format(self.waveform_formats[waveform_format]))

    def waveform_points(self, points: int):
        """ Sets the number of points to be taken from the waveform data """
        self.resource.write(":WAV:POINT {}".format(points))

    def waveform_data(self):
        """ Returns the waveform data """
        return self.resource.query(":WAV:DATA?")

    def waveform_preamble(self):
        """ Returns the waveform data preamble used to decode byte data """
        return self.resource.query(":WAV:PRE?")

    #####################
    # DIGITIZE COMMANDS #
    #####################

    def digitize(self, source: Sources):
        """ Acquires the waveform of a selected channel using the current settings. """
        self.resource.write(":DIG {}".format(self.sources[source]))


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


# Subscribing the new instrument to the lab-tool register
LabTool.add_oscilloscope(AgilentDSO6014)
