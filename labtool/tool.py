"""
LabTool module with a list of the available devices
"""

# python native modules
from enum import Enum
from math import log10

# third-party modules
import pyvisa
import xlwt

# labtool project modules
from labtool.oscilloscope.base.oscilloscope import Oscilloscope
from labtool.generator.base.generator import Generator

from labtool.oscilloscope.base.oscilloscope import Sources

from labtool.generator.base.generator import Waveform
from labtool.generator.base.generator import OutputLoad
from labtool.generator.base.generator import OutputMode

from labtool.base.instrument import InstrumentType
from labtool.base.instrument import Instrument


############################
# LabTool Enum Definitions #
############################

class BodeScale(Enum):
    Linear = "Linear"
    Log = "Log"


######################
# LabTool Exceptions #
######################

class DeviceNotFound(Exception):
    def __init__(self):
        super(DeviceNotFound, self).__init__("Could not find any device with the given instrument type."
                                             + " Verify the device connection or if the module has been imported.")


###################################
# LabTool static class definition #
###################################

class LabTool(object):
    """ LabTool static methods """

    # Available devices in the LabTool
    available_oscilloscopes = []
    available_generators = []

    # Internal LabTool definitions
    class BodeStates(Enum):
        """ Internal states for defining a Bode simple FSM
        when working with the oscilloscope and the generator. """
        INITIAL_SETUP = "Initial setup"
        STEP_SETUP = "Step setup"
        DOWNLOAD_DATA = "Download data"
        DONE = "Done"

    @staticmethod
    def open_device(instrument_type: InstrumentType) -> Instrument:
        """ open_device() returns an instance of an Instrument interface by detecting all connected models.
            IMPORTANT! In order to detect instruments, devices should be imported for
            LabTool to be able to detect them.

            Note: This first version runs opening any detected device corresponding with the intrsument type.

            [OPTIONS]
                + instrument_type: What kind of instrument should be detected
                """
        # Creating the resource manager and interface
        resource_manager = pyvisa.ResourceManager()
        resources = resource_manager.list_resources()
        for resource in resources:
            # Requesting the standard visa identification code
            interface = resource_manager.open_resource(resource)
            model_name = interface.query("*IDN?").split(",")[1]
            interface.close()
            # Searching an interface for that device model
            if instrument_type is InstrumentType.Oscilloscope:
                for oscilloscope in LabTool.available_oscilloscopes:
                    if oscilloscope.model == model_name:
                        return oscilloscope(resource)
            elif instrument_type is InstrumentType.Generator:
                for generator in LabTool.available_generators:
                    if generator.model == model_name:
                        return generator(resource)

        # Raising exception...
        raise DeviceNotFound

    @staticmethod
    def add_oscilloscope(oscilloscope):
        """ Registers a new Oscilloscope Class """
        LabTool.available_oscilloscopes.append(oscilloscope)

    @staticmethod
    def add_generator(generator):
        """ Registers a new Generator Class """
        LabTool.available_generators.append(generator)

    @staticmethod
    def download_waveform(oscilloscope,
                          source,
                          waveform_format):
        """ Returns the waveform data from the given channel in the
        oscilloscope.
        Note: In this initial version of the LabTool,
        both preamble and data are returned so as to know what the
        oscilloscope is returning for those queries. """
        oscilloscope.digitize(source)
        oscilloscope.waveform_source(source)
        oscilloscope.waveform_format(waveform_format)
        oscilloscope.waveform_unsigned(True)
        oscilloscope.waveform_points(10000)

        preamble = oscilloscope.waveform_preamble()
        data = oscilloscope.waveform_data()

        return {
            "preamble": preamble,
            "data": data
        }

    @staticmethod
    def horizontal_scale(oscilloscope: Oscilloscope, input_channel: Sources, output_channel: Sources, frequency: float):
        """ Auto scaling the horizontal axis of the Oscilloscope for the given source """
        periods = 2
        scale_complete = False
        while not scale_complete:
            current_phase = float(oscilloscope.measure_phase(output_channel, input_channel))
            if -180 < current_phase < 180:
                scale_complete = True
            else:
                oscilloscope.set_timebase_range(periods / frequency)
                periods += 1

    @staticmethod
    def vertical_scale(oscilloscope: Oscilloscope, source: Sources):
        """ Auto scaling the vertical axis of the Oscilloscope for the given source """
        margin = 0.1
        pattern = [10, 20, 50]
        current = 0
        scale_complete = False
        while not scale_complete:
            signal_vpp = float(oscilloscope.measure_vpp(source))
            channel_vpp = float(oscilloscope.get_range(Oscilloscope.source_to_channel(source)))
            if signal_vpp < channel_vpp:
                oscilloscope.set_range(Oscilloscope.source_to_channel(source), signal_vpp * (1 + margin))
                scale_complete = True
            else:
                oscilloscope.set_scale(Oscilloscope.source_to_channel(source), pattern[current])
                current += 1

    @staticmethod
    def compute_frequency(step: int, bode_setup: dict):
        min_frequency = bode_setup["start-frequency"]
        max_frequency = bode_setup["stop-frequency"]
        samples = bode_setup["samples"]

        beta = min_frequency
        alpha = (max_frequency - min_frequency) / log10(samples)

        if bode_setup["scale"] is BodeScale.Linear:
            result = (max_frequency - min_frequency) * step / samples + min_frequency
        elif bode_setup["scale"] is BodeScale.Log:
            result = alpha * log10(step + 1) + beta
        return result

    @staticmethod
    def run_bode(
            osc: Oscilloscope, gen: Generator,
            bode_setup: dict,
            generator_setup: dict,
            trigger_setup: dict,
            timebase_setup: dict,
            acquire_setup: dict,
            input_channel: Sources, input_channel_setup: dict,
            output_channel: Sources, output_channel_setup: dict):
        """ Runs an automatic bode measuring using the given Oscilloscope and Generator.

        [Bode Setup]
            + delay: seconds between every step
            + scale: scale used to compute frequency
            + start-frequency: start point frequency
            + stop-frequency: stop point frequency
            + samples: number of samples taken between the start and the stop frequency

        [Generator Setup]
            + amplitude: starting amplitude value

        [Return] Returns a list of dictionaries containing for each frequency,
        the input and output voltage values, the module and phase of the frequency
        response.
            return = [
                {
                    "frequency": value_of_frequency,
                    "input-vpp": value_of_input_amplitude,
                    "output-vpp": value_of_output_amplitude,
                    "bode-module": value_of_bode_module,
                    "bode-phase": value_of_bode_phase
                }
            ]
        """

        # Bode setup parameter validation, raising exception
        # when not receiving the needed input data
        for dependency in ["delay", "start-frequency", "stop-frequency", "samples"]:
            if dependency not in bode_setup.keys():
                raise ValueError("Bode setup data is not complete. Missing: {}".format(dependency))

        # Initializing variables for running the fsm...
        bode_state = LabTool.BodeStates.INITIAL_SETUP
        bode_measures = []
        bode_step = 0

        # FSM working loop...
        while bode_state is not LabTool.BodeStates.DONE:
            if bode_state is LabTool.BodeStates.INITIAL_SETUP:
                osc.reset()
                osc.setup_channel(osc.source_to_channel(input_channel), **input_channel_setup)
                osc.setup_channel(osc.source_to_channel(output_channel), **output_channel_setup)
                osc.setup_trigger(**trigger_setup)
                osc.setup_timebase(**timebase_setup)
                osc.setup_acquire(**acquire_setup)
                osc.set_delay(bode_setup["delay"])

                gen.reset()
                gen.set_waveform(Waveform.Sine)
                gen.set_frequency(LabTool.compute_frequency(bode_step, bode_setup))
                gen.set_output_load(None, OutputLoad.HighZ)
                gen.set_amplitude(generator_setup["amplitude"])
                gen.set_output_mode(OutputMode.ON)

                bode_state = LabTool.BodeStates.STEP_SETUP

            elif bode_state is LabTool.BodeStates.STEP_SETUP:
                gen.set_frequency(LabTool.compute_frequency(bode_step, bode_setup))
                osc.set_timebase_range(2 / LabTool.compute_frequency(bode_step, bode_setup))

                LabTool.vertical_scale(osc, input_channel)
                LabTool.vertical_scale(osc, output_channel)
                LabTool.horizontal_scale(
                    osc,
                    input_channel, output_channel,
                    LabTool.compute_frequency(bode_step, bode_setup)
                )

                bode_state = LabTool.BodeStates.DOWNLOAD_DATA

            elif bode_state is LabTool.BodeStates.DOWNLOAD_DATA:
                input_vpp = float(osc.measure_vpp(input_channel))
                output_vpp = float(osc.measure_vpp(output_channel))
                ratio = float(osc.measure_vratio(output_channel, input_channel))
                phase = float(osc.measure_phase(output_channel, input_channel))
                bode_measures.append(
                    {
                        "frequency": LabTool.compute_frequency(bode_step, bode_setup),
                        "input-vpp": input_vpp,
                        "output-vpp": output_vpp,
                        "bode-module": ratio,
                        "bode-phase": phase
                    }
                )

                bode_step += 1
                if bode_step >= bode_setup["samples"]:
                    bode_state = LabTool.BodeStates.DONE
                else:
                    bode_state = LabTool.BodeStates.STEP_SETUP

        # Finished without errors, returning the result!
        return bode_measures

    @staticmethod
    def export_to_csv(filepath: str, bode_measures: list):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Bode")

        for index, header in enumerate(["Frequency [Hz]", "Input VPP", "Output VPP", "Bode Module [dB]", "Bode Phase [°]"]):
            sheet.write(0, index, header)

        for measure_index, measure in enumerate(bode_measures):
            row = [
                    measure["frequency"],
                    measure["input-vpp"],
                    measure["output-vpp"],
                    measure["bode-module"],
                    measure["bode-phase"]
            ]

            for element_index, element in enumerate(row):
                sheet.write(measure_index + 1, element_index, element)

        workbook.save("{}.xls".format(filepath))
