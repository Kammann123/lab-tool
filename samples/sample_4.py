"""
Sample_4: Testing the compute_frequency() algorithms when using Log or Linear.
"""

# labtool project modules
from labtool.tool import LabTool
from labtool.tool import BodeScale

# third-party modules
from matplotlib import pyplot

if __name__ == "__main__":

    bode_setup = {
        "start-frequency": 10,
        "stop-frequency": 1000000,
        "samples": 100,
        "scale": BodeScale.Log
    }

    values = [i + 1 for i in range(100)]
    frequency = [LabTool.compute_frequency(value, bode_setup) for value in values]

    pyplot.plot(values, frequency)
    pyplot.show()
