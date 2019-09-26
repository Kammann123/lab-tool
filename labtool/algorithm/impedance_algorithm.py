# python native modules
import cmath
import numpy

# third-party modules

# labtool project modules
from labtool.algorithm.bode_algorithm import BodeAlgorithm


class ImpedanceAlgorithm(BodeAlgorithm):

    def __call__(self):
        """ Runs an automatic input impedance measuring using the given Oscilloscope and Generator.
            [Return] Returns a list of dictionaries containing for each frequency,
                the generator and input voltage values and its phase. The impedance and its phase.
                    return = [
                        {
                            "frequency": value_of_frequency,
                            "generator-vpp": value_of_input_amplitude,
                            "input-vpp": value_of_output_amplitude,
                            "input-phase": value_of_output_phase,
                            "impedance-module": value_of_impedance_module,
                            "impedance-phase": value_of_impedance_phase
                        }
                    ]
        """
        # Executes the BodeAlgorithm!
        self.buffer = self.requirements
        self.requirements = {
            "input-channel": self.buffer["generator-channel"],
            "output-channel": self.buffer["input-channel"]
        }
        bode_measures = BodeAlgorithm.__call__(self)
        self.requirements = self.buffer
        impedance_measures = []

        for bode_measure in bode_measures:
            v_gen = cmath.rect(bode_measure["input-vpp"], 0)
            v_in = cmath.rect(bode_measure["output-vpp"], numpy.radians(bode_measure["output-phase"]))
            z = (v_in * self.requirements["resistance"]) / (v_gen - v_in)

            impedance_measures.append(
                {
                    "frequency": bode_measure["frequency"],
                    "generator-vpp": bode_measure["input-vpp"],
                    "input-vpp": bode_measure["output-vpp"],
                    "input-phase": bode_measure["output-phase"],
                    "impedance-module": abs(z),
                    "impedance-phase": numpy.degrees(cmath.phase(z))
                }
            )

        return impedance_measures

    def what(self):
        return "Measuring input impedance of the system"
