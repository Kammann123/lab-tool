# python native modules
from enum import Enum

import cmath
import numpy

# third-party modules

# labtool project modules
from labtool.algorithm.bode_algorithm import BodeAlgorithm


class ImpedanceAlgorithm(BodeAlgorithm):

    def __init__(self, *args, **kwargs):
        super(ImpedanceAlgorithm, self).__init__(*args, **kwargs)

        self.impedance_requirements = self.requirements
        self.requirements = {
            "input-channel": self.impedance_requirements["generator-channel"],
            "output-channel": self.impedance_requirements["input-channel"]
        }

    def get_result(self):
        impedance_measures = []
        for bode_measure in self.result:
            v_gen = cmath.rect(bode_measure["input-vpp"], 0)
            v_in = cmath.rect(bode_measure["output-vpp"], numpy.radians(bode_measure["bode-phase"]))
            z = (v_in * self.impedance_requirements["resistance"]) / (v_gen - v_in)

            impedance_measures.append(
                {
                    "frequency": bode_measure["frequency"],
                    "generator-vpp": bode_measure["input-vpp"],
                    "input-vpp": bode_measure["output-vpp"],
                    "input-phase": bode_measure["bode-phase"],
                    "impedance-module": abs(z),
                    "impedance-phase": numpy.degrees(cmath.phase(z))
                }
            )

        return impedance_measures

    def what(self):
        return "Measuring input impedance of the system"
