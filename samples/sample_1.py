"""
Sample_1: First attempt to writing a python script in order to open a resource
and trying to configure it, assuming it is an oscilloscope.
"""

# third-party modules
import pyvisa


def console(message: str):
    """ console() printing message with fancy style. """
    print(
        "[lab-tool] >> {}".format(message)
    )


def resources_to_console(res: tuple):
    """ Formatting a message to display the resources """
    message = "{} resources have been detected \n".format(len(res))
    for index, resource in enumerate(res):
        message += "\t [{}] = {} \n".format(index, resource)
    console(message)


if __name__ == "__main__":

    # Instance of ResourceManager, check the resources and show them
    manager = pyvisa.ResourceManager()
    resources = manager.list_resources()
    resources_to_console(resources)

    try:
        # Device selection
        index = int(input("[lab-tool] >> Device selection: "))

        # Setting up the oscilloscope
        console("Opening the {} device...".format(resources[index]))
        resource = manager.open_resource(resources[index])
        resource.query("*RST")

    except:
        console("Invalid input... nicely done! I give up.")
