"""
LabTool module with a list of the available devices
"""

# python native modules
from enum import Enum
from time import sleep

# labtool project modules
from labtool.oscilloscope.base.oscilloscope import Oscilloscope
from labtool.generator.base.generator import Generator

from labtool.oscilloscope.base.oscilloscope import Sources

from labtool.generator.base.generator import Waveform
from labtool.generator.base.generator import OutputLoad


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
    def source_scale(oscilloscope: Oscilloscope, source: Sources):
        constant_limit = 1e3
        pattern_value = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]
        current_value = 0
        while True:
            source_vpp = float(oscilloscope.measure_vpp(source))
            if abs(source_vpp) < constant_limit:
                break
            else:
                oscilloscope.scale(Oscilloscope.source_to_channel(source), pattern_value[current_value])
                current_value += 1
                sleep(0.1)

    @staticmethod
    def compute_frequency(step: int, bode_setup: dict):
        min_frequency = bode_setup["start_frequency"]
        max_frequency = bode_setup["stop_frequency"]
        samples = bode_setup["samples"]
        return (max_frequency - min_frequency) * step / samples + min_frequency

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
                osc.setup_channel(osc.source_to_channel(input_channel), **input_channel_setup)
                osc.setup_channel(osc.source_to_channel(output_channel), **output_channel_setup)
                osc.setup_trigger(**trigger_setup)
                osc.setup_timebase(**timebase_setup)
                osc.setup_acquire(**acquire_setup)

                gen.set_waveform(Waveform.Sine)
                gen.set_frequency(LabTool.compute_frequency(bode_step, bode_setup))
                gen.set_output_load(None, OutputLoad.HighZ)
                gen.set_amplitude(generator_setup["amplitude"])

                bode_state = LabTool.BodeStates.STEP_SETUP

            elif bode_state is LabTool.BodeStates.STEP_SETUP:
                gen.set_frequency(LabTool.compute_frequency(bode_step, bode_setup))
                osc.timebase_range(2 / LabTool.compute_frequency(bode_step, bode_setup))

                LabTool.source_scale(osc, input_channel)
                LabTool.source_scale(osc, output_channel)

                sleep(bode_setup["delay"])
                bode_state = LabTool.BodeStates.DOWNLOAD_DATA

            elif bode_state is LabTool.BodeStates.DOWNLOAD_DATA:
                input_vpp = float(osc.measure_vpp(input_channel))
                output_vpp = float(osc.measure_vpp(output_channel))
                ratio = float(osc.measure_vratio(output_channel, input_channel))
                phase = float(osc.measure_phase(output_channel, input_channel))
                bode_measures.append(
                    {
                        "frequency": current_frequency,
                        "input-vpp": input_vpp,
                        "output-vpp": output_vpp,
                        "bode-module": ratio,
                        "bode-phase": phase
                    }
                )

                bode_step += 1
                if bode_step >= bode_step["samples"]:
                    bode_state = LabTool.BodeStates.DONE
                else:
                    bode_state = LabTool.BodeStates.STEP_SETUP

        # Finished without errors, returning the result!
        return bode_measures
