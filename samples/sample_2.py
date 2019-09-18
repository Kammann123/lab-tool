"""
Sample_2: Running the first version of the LabTool package and using the interpreter console
as a user interface for interacting.
"""

# python native modules

# third-party modules
from matplotlib import pyplot

import pyvisa

# labtool project modules
from labtool.base.instrument import Instrument
from labtool.base.instrument import InstrumentType

from labtool.oscilloscope.base.oscilloscope import Sources

from labtool.oscilloscope.base.oscilloscope import BandwidthLimit
from labtool.oscilloscope.base.oscilloscope import Coupling

from labtool.oscilloscope.base.oscilloscope import TriggerMode
from labtool.oscilloscope.base.oscilloscope import TriggerSweep
from labtool.oscilloscope.base.oscilloscope import TriggerSlope

from labtool.oscilloscope.base.oscilloscope import TimebaseMode

from labtool.oscilloscope.base.oscilloscope import AcquireMode

from labtool.tool import LabTool
from labtool.tool import BodeScale

# Loading the available devices into the LabTool package
from labtool.oscilloscope.agilent.agilent_dso6014A import AgilentDSO6014
from labtool.generator.agilent.agilent_33220a import Agilent33220A


###############################
# Interface utility functions #
###############################

def console(message: str):
    """ console() printing message with fancy style. """
    print(
        "[lab-tool] >> {}".format(message)
    )


def console_separator():
    """ Prints in the console, using the console() routine, a separator """
    console(
        "---------------------------------------------------------------------------------------------------------" +
        "\n\n"
    )


def resources_to_console(res: tuple):
    """ Formatting a message to display the resources """
    message = "{} resources have been detected \n".format(len(res))
    for index, resource in enumerate(res):
        message += "\t [{}] = {} \n".format(index, resource)
    console(message)


def instruments_to_console():
    """ Formatting a message to display the available instruments in the LabTool package. """
    message = "{} oscilloscope models available detected: \n".format(
        len(LabTool.available_oscilloscopes)
    )
    last_index = 0
    for index, osc in enumerate(LabTool.available_oscilloscopes):
        message += "\t [{}] = {} {} \n".format(index, osc.brand, osc.model)
        last_index = index
    message += "{} generators models available detected: \n".format(
        len(LabTool.available_generators)
    )
    for index, gen in enumerate(LabTool.available_generators):
        message += "\t [{}] = {} {} \n".format(index + last_index, gen.brand, gen.model)
    console(message)


if __name__ == "__main__":
    console("Welcome to the LabTool! In order to measure a bode diagram, you will need an oscilloscope and a generator.")

    # Opening needed devices
    oscilloscope = LabTool.open_device_by_type(InstrumentType.Oscilloscope)
    generator = LabTool.open_device_by_type(InstrumentType.Generator)

    # Setup or configuration objects
    input_channel_setup = output_channel_setup = {
        "bandwidth_limit": BandwidthLimit.OFF,
        "coupling": Coupling.DC,
        "probe": 10,
        "display": True,
        "range": 20,
        "offset": 0
    }

    trigger_setup = {
        "trigger-mode": TriggerMode.Edge,
        "trigger-sweep": TriggerSweep.Auto,
        "trigger-edge-level": 0,
        "trigger-edge-slope": TriggerSlope.Positive,
        "trigger-edge-source": Sources.Channel_1,
        "hf-reject": True,
        "n-reject": True
    }

    timebase_setup = {
        "timebase-mode": TimebaseMode.Main
    }

    acquire_setup = {
        "acquire-mode": AcquireMode.Average,
        "average-count": 2
    }

    # When using BodeScale.Log mode, only start-frequency,
    # and samples matter, when using BodeScale.Linear, all
    # the start, stop and samples are important.
    bode_setup = {
        "delay": 0.1,
        "stable-time": 0.1,
        "scale": BodeScale.Log,
        "start-frequency": 10,
        "stop-frequency": 40000,
        "samples": 20
    }

    generator_setup = {
        "amplitude": 20
    }

    # Setting the LabTool run_bode() routine
    measures = LabTool.run_bode(
        oscilloscope, generator,
        bode_setup,
        generator_setup,
        trigger_setup,
        timebase_setup,
        acquire_setup,
        Sources.Channel_1, input_channel_setup,
        Sources.Channel_2, output_channel_setup
    )

    frequency = [measure["frequency"] for measure in measures]
    module = [measure["bode-module"] for measure in measures]
    phase = [measure["bode-phase"] for measure in measures]

    pyplot.semilogx(frequency, module)
    pyplot.show()

    filepath = input("Enter the name of the output excel file: ")
    LabTool.export_to_csv(filepath, measures)

    input("Press any key...")
