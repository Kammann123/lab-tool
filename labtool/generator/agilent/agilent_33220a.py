"""
Agilent 33220A signal generator class implementation.
"""

# labtool project modules
from labtool.tool import LabTool

from labtool.generator.base.generator import Generator
from labtool.generator.base.generator import Waveform
from labtool.generator.base.generator import OutputMode
from labtool.generator.base.generator import SyncMode
from labtool.generator.base.generator import OutputPolarity
from labtool.generator.base.generator import OutputLoad


#######################
# Agilent model class #
#######################

class Agilent33220A(Generator):
    """ Agilent 33220A generator model """

    # Instrument information
    brand = "AGILENT"
    model = "33220A"

    # Internal dictionaries of agilent syntax
    waveforms = {
        Waveform.Sine: "SINusoid",
        Waveform.Square: "SQUare",
        Waveform.Ramp: "RAMP"
    }

    output_modes = {
        OutputMode.OFF: "OFF",
        OutputMode.ON: "ON"
    }

    sync_modes = {
        SyncMode.OFF: "OFF",
        SyncMode.ON: "ON"
    }

    output_polarities = {
        OutputPolarity.Normal: "NORMal",
        OutputPolarity.Inverted: "INVerted"
    }

    output_loads = {
        OutputLoad.Value: "Value",
        OutputLoad.HighZ: "INFinity"
    }

    ###################
    # COMMON COMMANDS #
    ###################

    def reset(self):
        """ Resets the generator. """
        self.resource.write("*RST")

    def clear(self):
        """ Clears the generator's status registers. """
        self.resource.write("*CLS")

    def who(self) -> str:
        """ Returns a string with an generator's identifier. """
        return self.resource.query("*IDN?")

    ##################
    # APPLY COMMANDS #
    ##################

    def generate_signal(self, **kwargs):
        """ Generates a signal controlled by received parameters
            [Options]
                + waveform: Waveform
                + frequency: Frequency value
                + amplitude: Amplitude value
                + offset: Offset value
                """
        for dependency in ["waveform", "frequency", "amplitude", "offset"]:
            if dependency not in kwargs.keys():
                raise ValueError("Option dependency needed to run the generate_signal() routine: {}".format(dependency))

        self.resource.write(
            "APPLy:{} {}, {}, {}".format(
                self.waveforms[kwargs["waveform"]],
                kwargs["frequency"],
                kwargs["amplitude"],
                kwargs["offset"])
        )

    ############################
    # OUTPUT CONFIG COMMANDS   #
    ############################

    def set_waveform(self, waveform: Waveform):
        """Changes output waveform type, selectable from the ones in Enum"""
        self.resource.write("FUNCtion {}".format(self.waveforms[waveform]))

    def set_frequency(self, frequency: float):
        """ Changes output frequency """
        self.resource.write("FREQuency {}".format(frequency))

    def set_amplitude(self, amplitude: float):
        """ Changes output amplitude """
        self.resource.write("VOLTage {}".format(amplitude))

    def set_offset(self, offset: float):
        """Changes output offset"""
        self.resource.write("OFFSet {}".format(offset))

    def set_square_duty(self, percent: float):
        """Changes output duty cycle, only applicable if output is Square"""
        self.resource.write("FUNCtion:{}:DCYCle {}".format(self.waveforms[Waveform.Square], percent))

    def set_ramp_symmetry(self, percent: float):
        """Changes output symmetry, only applicable if output is Ramp"""
        self.resource.write("FUNCtion:{}:SYMMetry {}".format(self.waveforms[Waveform.Ramp], percent))

    def set_output_mode(self, mode: OutputMode):
        """Turns the output on or off depending on the arg"""
        self.resource.write("OUTPut {}".format(self.output_modes[mode]))

    def check_output_mode(self) -> OutputMode:
        """Returns a OutputMode indicating output state"""
        return self.resource.query("OUTPut?")

    def set_output_pol(self, polarity: OutputPolarity):
        """Changes output polarity"""
        self.resource.write("OUTPut:POLarity {}".format(self.output_polarities[polarity]))

    def check_output_polarity(self) -> OutputPolarity:
        """Returns a OutputPolarity indicating output polarity"""
        return self.resource.query("OUTPut:POLarity?")

    def set_output_load(self, load: float, load_param: OutputLoad):
        """Changes output load. It can be a fixed value or HighZ"""
        if load_param == OutputLoad.HighZ:
            self.resource.write("OUTPut:LOAD {}".format(self.output_loads[load_param]))
        else:
            self.resource.write("OUTPut:LOAD {}".format(load))

    def check_output_load(self) -> (float, OutputLoad):
        """Returns a tuple including a value and OutputLoad, if OutputLoad == OutputLoad.HighZ
            value contents have no sense"""
        return self.resource.query("OUTPut:LOAD?")

    def set_sync_mode(self, mode: SyncMode):
        """Turns the Sync output on or off depending on the arg"""
        self.resource.write("OUTPut:SYNC {}".format(self.sync_modes[mode]))

    def check_sync_mode(self) -> SyncMode:
        """Returns a OutputMode indicating output state"""
        return self.resource.query("OUTPut:SYNC?")


# Subscribing the new instrument to the lab-tool register
LabTool.add_generator(Agilent33220A)
