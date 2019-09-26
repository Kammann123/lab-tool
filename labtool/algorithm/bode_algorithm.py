# python native modules
from enum import Enum
from time import sleep

# third-party modules

# labtool project modules
from labtool.algorithm.base.measure_algorithm import MeasureAlgorithm
from labtool.tool import BodeScale


class BodeStates(Enum):
    """ Internal states for defining a Bode simple FSM
    when working with the oscilloscope and the generator. """
    INITIAL_SETUP = "Initial setup"
    STEP_SETUP = "Step setup"
    DOWNLOAD_DATA = "Download data"
    DONE = "Done"


class BodeAlgorithm(MeasureAlgorithm):

    def compute_frequency(self, step: int):
        min_frequency = self.preferences_setup["start-frequency"]
        max_frequency = self.preferences_setup["stop-frequency"]
        samples = self.preferences_setup["samples"]

        frequencies = list(logspace(log10(min_frequency), log10(max_frequency), num=samples))

        if self.preferences_setup["scale"] is BodeScale.Linear:
            result = (max_frequency - min_frequency) * step / samples + min_frequency
        elif self.preferences_setup["scale"] is BodeScale.Log:
            result = frequencies[step]
        else:
            raise ValueError

        return result

    def horizontal_scale(self, frequency: float):
        """ Auto scaling the horizontal axis of the Oscilloscope for the given source """
        periods = 3
        scale_complete = False
        while not scale_complete:
            current_phase = float(
                self.oscilloscope.measure_phase(
                    self.preferences_setup["output-channel"],
                    self.preferences_setup["input-channel"]
                )
            )

            if -180 < current_phase < 180:
                scale_complete = True
            else:
                self.oscilloscope.set_timebase_range(periods / frequency)
                periods += 1

    def vertical_scale(self, source: Sources):
        """ Auto scaling the vertical axis of the Oscilloscope for the given source """
        margin = 0.1
        pattern = [1, 2, 5, 10, 20, 50]
        current = 0
        scale_complete = False
        while not scale_complete:
            signal_vpp = max(
                float(self.oscilloscope.measure_vpp(source)),
                float(self.oscilloscope.measure_vmax(source)),
                float(self.oscilloscope.measure_vmin(source))
            )
            channel_vpp = float(self.oscilloscope.get_range(Oscilloscope.source_to_channel(source)))
            if signal_vpp < channel_vpp:
                signal_vpp = float(self.oscilloscope.measure_vpp(source))
                self.oscilloscope.set_range(Oscilloscope.source_to_channel(source), signal_vpp * (1 + margin))
                scale_complete = True
            else:
                self.oscilloscope.set_scale(Oscilloscope.source_to_channel(source), pattern[current])
                current += 1

    def __call__(self):
        """ Runs an automatic bode measuring using the given Oscilloscope and Generator.
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
        # Initializing variables for running the fsm...
        bode_state = BodeStates.INITIAL_SETUP
        bode_measures = []
        bode_step = 0

        # FSM working loop...
        while bode_state is not BodeStates.DONE:
            if bode_state is BodeStates.INITIAL_SETUP:
                # self.progress.emit(0)

                self.oscilloscope.set_delay(self.preferences_setup["delay"])
                self.oscilloscope.reset()
                self.oscilloscope.autoscale()

                self.oscilloscope.setup_timebase(**self.timebase_setup)
                self.oscilloscope.setup_channel(self.oscilloscope.source_to_channel(self.requirements["input-channel"]), **self.channel_setup)
                self.oscilloscope.setup_channel(self.oscilloscope.source_to_channel(self.requirements["output-channel"]), **self.channel_setup)
                self.oscilloscope.setup_trigger(**self.trigger_setup)

                self.generator.reset()
                self.generator.set_waveform(Waveform.Sine)
                self.generator.set_frequency(self.compute_frequency(bode_step))
                self.generator.set_output_load(None, OutputLoad.HighZ)
                self.generator.set_amplitude(self.generator_setup["amplitude"])
                self.generator.set_output_mode(OutputMode.ON)

                bode_state = BodeStates.STEP_SETUP

            elif bode_state is BodeStates.STEP_SETUP:
                # self.progress.emit(bode_step * 100 / self.preferences_setup["samples"])

                self.generator.set_frequency(self.compute_frequency(bode_step))
                self.oscilloscope.set_timebase_range(2 / self.compute_frequency(bode_step))
                self.oscilloscope.set_acquire_mode(AcquireMode.Normal)

                self.vertical_scale(input_channel)
                self.vertical_scale(output_channel)
                self.horizontal_scale(self.compute_frequency(bode_step))

                sleep(self.preferences_setup["stable-time"])
                bode_state = BodeStates.DOWNLOAD_DATA

            elif bode_state is BodeStates.DOWNLOAD_DATA:
                self.oscilloscope.setup_acquire(**self.acquire_setup)

                input_vpp = float(self.oscilloscope.measure_vpp(input_channel))
                output_vpp = float(self.oscilloscope.measure_vpp(output_channel))
                ratio = float(self.oscilloscope.measure_vratio(output_channel, input_channel))
                phase = float(self.oscilloscope.measure_phase(output_channel, input_channel))
                bode_measures.append(
                    {
                        "frequency": self.compute_frequency(bode_step),
                        "input-vpp": input_vpp,
                        "output-vpp": output_vpp,
                        "bode-module": ratio,
                        "bode-phase": phase
                    }
                )

                bode_step += 1
                if bode_step >= self.preferences_setup["samples"]:
                    bode_state = BodeStates.DONE
                    # self.progress.emit(100)
                else:
                    bode_state = BodeStates.STEP_SETUP

        # Filtering error values
        bode_aux = []
        for bode_measure in bode_measures:
            if bode_measure["bode-module"] > 1e3 or bode_measure["bode-phase"] > 1e3:
                continue
            bode_aux.append(bode_measure)
        bode_measures = bode_aux

        # Finished without errors, returning the result!
        return bode_measures

    def what(self):
        return "Measuring bode plots of the system"
