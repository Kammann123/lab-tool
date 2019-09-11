"""
LabTool module with a list of the available devices
"""

# python native modules
from enum import Enum
from time import sleep

# labtool project modules
from labtool.oscilloscope.base.oscilloscope import ChannelSetup
from labtool.oscilloscope.base.oscilloscope import TriggerSetup
from labtool.oscilloscope.base.oscilloscope import TimebaseSetup
from labtool.oscilloscope.base.oscilloscope import AcquireSetup

from labtool.oscilloscope.base.oscilloscope import Sources

from labtool.oscilloscope.base.oscilloscope import Oscilloscope


#########################
# LabTool project types #
#########################

class BodeSetup(object):
    """ Container class for the parameter values of the setup
    for a run_bode() routine of the LabTool package. """

    def __init__(self,
                 min_frequency: float,
                 max_frequency: float,
                 number_samples: int):
        self.min_frequency = min_frequency
        self.max_frequency = max_frequency
        self.samples = number_samples

    def compute_frequency(self, step: int):
        return (self.max_frequency - self.min_frequency) * step / self.samples + self.min_frequency


###################################
# LabTool static class definition #
###################################

class LabTool(object):
    """ LabTool static methods b b """

    # Available devices in the LabTool
    available_oscilloscopes = []
    available_generators = []

    # Internal LabTool definitions
    class BodeStates(Enum):
        """ Internal states for defining a Bode simple FSM
        when working with the oscilloscope and the generator. """
        INITIAL_SETUP = "Initial setup"
        STEP_SETUP = "Step setup"
        WAIT_STABLE = "Wait stable"
        DOWNLOAD_DATA = "Download data"
        VERIFY_DONE = "Verify done"
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
        range_value = 50

        source_vpp = float(oscilloscope.measure_vpp(source))
        while abs(source_vpp) > constant_limit:
            oscilloscope.range(Oscilloscope.source_to_channel(source), range_value)
            range_value -= 10
            sleep(0.01)
            source_vpp = float(oscilloscope.measure_vpp(source))

    @staticmethod
    def run_bode(oscilloscope,
                 generator,
                 delay: float,
                 input_voltage: float,
                 input_channel: Sources,
                 output_channel: Sources,
                 input_channel_setup: ChannelSetup,
                 output_channel_setup: ChannelSetup,
                 trigger_setup: TriggerSetup,
                 timebase_setup: TimebaseSetup,
                 acquire_setup: AcquireSetup,
                 bode_setup: BodeSetup
                 ):
        """ Runs an automatic bode measuring using the given Oscilloscope and
        Generator.

        Note: the generator amplitude is considered a constant value. Should be checking whether it
        saturates or not.

        [Parameters]
            * delay_ticks: The number of the periods that should be waited.

        [Return] Returns a list of dictionaries containing for each frequency,
        the input and output voltage values, the module and phase of the frequency
        response.
            return = [
                {
                    "frequency": value_of_frequency,
                    "input_vpp": value_of_input_amplitude,
                    "output_vpp": value_of_output_amplitude,
                    "bode_module": value_of_bode_module,
                    "bode_phase": value_of_bode_phase
                }
            ]
        """

        # Setting up things to run a simple fsm
        bode_state = LabTool.BodeStates.INITIAL_SETUP

        current_frequency = bode_setup.min_frequency
        current_amplitude = input_voltage
        current_step = 1

        measures = []

        # FSM working loop...
        while bode_state is not LabTool.BodeStates.DONE:

            if bode_state is LabTool.BodeStates.INITIAL_SETUP:
                # Configuring the input channel
                oscilloscope.setup_channel(
                    oscilloscope.source_to_channel(input_channel),
                    input_channel_setup)

                # Configuring the output channel
                oscilloscope.setup_channel(
                    oscilloscope.source_to_channel(output_channel),
                    output_channel_setup)

                # Configuring the trigger subsystem
                oscilloscope.setup_trigger(trigger_setup)

                # Configuring the timebase subsystem
                oscilloscope.setup_timebase(timebase_setup)

                # Configuring the acquire subsystem
                oscilloscope.setup_acquire(acquire_setup)

                # Configuring the waveform generator
                # TODO: Charlie! Configurate las cosas iniciales del oscilador
                # TODO: como podria ser la forma de onda y cosas que no van a
                # TODO: cambiar... amplitud es input_voltage

                # State change
                bode_state = LabTool.BodeStates.STEP_SETUP

            elif bode_state is LabTool.BodeStates.STEP_SETUP:

                # For the current step, compute the needed values to
                # be set in the instruments...
                current_frequency = bode_setup.compute_frequency(current_step)
                current_voltage = input_voltage

                # Setting the range of the timebase
                oscilloscope.timebase_range(2 / current_frequency)
                LabTool.source_scale(oscilloscope, input_channel)
                LabTool.source_scale(oscilloscope, output_channel)

                # TODO: Charlie! Agregar la llamada para actualizar el valor pico a pico y la frecuencia,
                # TODO: la amplitud puede parecer absurdo... por ahora. Son los dos current_ de arriba!.

                # State change
                bode_state = LabTool.BodeStates.WAIT_STABLE

            elif bode_state is LabTool.BodeStates.WAIT_STABLE:

                # Waiting a period tick, then checking if finished...
                sleep(delay)

                # State change
                bode_state = LabTool.BodeStates.DOWNLOAD_DATA

            elif bode_state is LabTool.BodeStates.DOWNLOAD_DATA:

                # Retrieving data from the oscilloscope
                input_vpp = float(oscilloscope.measure_vpp(input_channel))
                output_vpp = float(oscilloscope.measure_vpp(output_channel))
                ratio = float(oscilloscope.measure_vratio(output_channel, input_channel))
                phase = float(oscilloscope.measure_phase(output_channel, input_channel))

                # Appending measurents to data list
                measures.append(
                    {
                        "frequency": current_frequency,
                        "input_vpp": input_vpp,
                        "output_vpp": output_vpp,
                        "bode_module": ratio,
                        "bode_phase": phase
                    }
                )

                # Bode state change
                bode_state = LabTool.BodeStates.VERIFY_DONE

            elif bode_state is LabTool.BodeStates.VERIFY_DONE:
                # Verifying if the number of samples taken is the one set
                if current_step == bode_setup.samples:
                    bode_state = LabTool.BodeStates.DONE
                else:
                    current_step += 1
                    bode_state = LabTool.BodeStates.STEP_SETUP

        return measures
