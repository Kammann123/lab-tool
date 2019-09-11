"""
Instrument Base Class to define a common or standard way to identify instruments.
"""

# third-party modules
import pyvisa


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


#########################
# Instrument Base Class #
#########################

class Instrument(object):
    """ Instrument base class """

    # Instrument information, static values for each class
    brand = "Instrument's Brand"
    model = "Instrument's Model"

    def __init__(self, resource_name):
        """ A Resource is opened and its reference will be saved, but if there is
        no resource with the given name or identifier, then an exception will be
        raised. """

        try:
            resource_manager = pyvisa.ResourceManager()
            self.resource = resource_manager.open_resource(resource_name)
        except:
            raise ResourceNotFound


