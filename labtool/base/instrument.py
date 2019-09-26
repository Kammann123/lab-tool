"""
Instrument Base Class to define a common or standard way to identify instruments.
"""

# python native modules
from enum import Enum

# third-party modules
import pyvisa

# labtool project modules
from labtool.base.delayed_resource import DelayedResource


################################
# Instrument module exceptions #
################################

class ResourceNotFound(Exception):
    def __init__(self):
        super(ResourceNotFound, self).__init__(
            "The given resource's name was not found in the Resource Manager"
        )


######################################
# Instrument enumeration definitions #
######################################

class InstrumentType(Enum):
    Oscilloscope = "Oscilloscope"
    Generator = "Generator"


#########################
# Instrument Base Class #
#########################

class Instrument(object):
    """ Instrument base class """

    # Higher ResourceManager control
    resource_manager = None

    # Instrument information, static values for each class
    brand = "Instrument's Brand"
    model = "Instrument's Model"
    type = "Instrument's Type"

    def __init__(self, resource_name):
        """ A Resource is opened and its reference will be saved, but if there is
        no resource with the given name or identifier, then an exception will be
        raised. """

        try:
            # Creating an instance of ResourceManager and opening the given resource
            resource_manager = pyvisa.ResourceManager() if Instrument.resource_manager is None else Instrument.resource_manager
            resource = resource_manager.open_resource(resource_name)

            # Setting up the resource
            resource.write_termination = "\n"
            resource.read_termination = "\n"
            self.resource = DelayedResource(resource)
        except:
            raise ResourceNotFound

    def __del__(self):
        """ Deleting the interface opened to interact with the given resource.
            Closing the visa connection.
         """
        self.resource.close()

        if Instrument.resource_manager is not None:
            Instrument.resource_manager.close()

    def set_delay(self, delay):
        self.resource.set_delay(delay)

    def close(self):
        self.resource.close()
