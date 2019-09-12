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
from labtool.oscilloscope.base.oscilloscope import Sources
from labtool.oscilloscope.base.oscilloscope import ChannelSetup

from labtool.tool import LabTool

# Loading the available devices into the LabTool package
from labtool.oscilloscope.agilent.agilent_dso6014 import AgilentDSO6014


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


def open_device() -> Instrument:
    """ Returns an instance of a Instrument selected by the user
    from the list of resources detected with the PyVisa package. """

    # Creating the ResourceManager instance and listing the resources
    resource_manager = pyvisa.ResourceManager()
    resources = resource_manager.list_resources()

    try:
        # Device selection
        console_separator()
        resources_to_console(resources)
        resources_selection = int(input("[lab-tool] >> Device selection: "))

        # Model selected
        console_separator()
        instruments_to_console()
        instrument_selection = int(input("[lab-tool] >> Instrument selection: "))

        # Instance building
        if instrument_selection < len(LabTool.available_oscilloscopes):
            builder = LabTool.available_oscilloscopes[instrument_selection]
        else:
            builder = LabTool.available_generators[instrument_selection - len(LabTool.available_oscilloscopes)]

        return builder(resources[resources_selection])
    except:
        console("I give up... \nHaha. Error in the input value! (Or some other thing... who knows)")


if __name__ == "__main__":
    console("Welcome to the LabTool! In order to measure a bode diagram, you will need an oscilloscope and a generator.")

    # Opening needed devices
    oscilloscope = open_device()

    from labtool.oscilloscope.base.oscilloscope import BandwidthLimit
    from labtool.oscilloscope.base.oscilloscope import Coupling

    from labtool.oscilloscope.base.oscilloscope import TriggerSetup
    from labtool.oscilloscope.base.oscilloscope import TriggerMode
    from labtool.oscilloscope.base.oscilloscope import TriggerSweep
    from labtool.oscilloscope.base.oscilloscope import TriggerSlope

    from labtool.oscilloscope.base.oscilloscope import TimebaseSetup
    from labtool.oscilloscope.base.oscilloscope import TimebaseMode

    from labtool.oscilloscope.base.oscilloscope import AcquireSetup
    from labtool.oscilloscope.base.oscilloscope import AcquireMode

    from labtool.tool import BodeSetup

    # Setup or configuration objects
    input_channel_setup = output_channel_setup = ChannelSetup(
        bandwidth_limit=BandwidthLimit.OFF,
        coupling=Coupling.DC,
        probe=10,
        display=True,
        range_value=20,
        offset=0
    )

    trigger_setup = TriggerSetup(
        mode=TriggerMode.Edge,
        sweep=TriggerSweep.Auto,
        level=0.01,
        slope=TriggerSlope.Positive,
        source=Sources.External
    )

    timebase_setup = TimebaseSetup(
        mode=TimebaseMode.Main
    )

    acquire_setup = AcquireSetup(
        acquire_mode=AcquireMode.Average,
        acquire_average_count=2
    )

    bode_setup = BodeSetup(
        10000,
        15000,
        5
    )

    # Setting the LabTool run_bode() routine
    measures = LabTool.run_bode(
        oscilloscope,
        None,
        0.2,
        20,
        Sources.Channel_1,
        Sources.Channel_2,
        input_channel_setup,
        output_channel_setup,
        trigger_setup,
        timebase_setup,
        acquire_setup,
        bode_setup
    )

    pyplot.plot([measure["frequency"] for measure in measures], [measure["bode_module"] for measure in measures])
    pyplot.plot([measure["frequency"] for measure in measures], [measure["bode_phase"] for measure in measures])
    pyplot.show()

    console("Press any key to exit...")
    input()
