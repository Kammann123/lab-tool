"""
DS4014 Rigol Model class implementation.
"""

# labtool project modules
from labtool.oscilloscope.agilent.agilent_dso6014A import *


#######################
# Agilent model class #
#######################

class RigolDS4014(AgilentDSO6014A):
    """ Rigol DS4014 Oscilloscope model """

    # Instrument information
    brand = "RIGOL"
    model = "DS4014"


# Subscribing the new instrument to the lab-tool register
LabTool.add_oscilloscope(RigolDS4014)
