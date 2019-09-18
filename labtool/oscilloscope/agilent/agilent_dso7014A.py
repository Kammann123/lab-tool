"""
DSO7014A Agilent Model class implementation.
"""

# labtool project modules
from labtool.oscilloscope.agilent.agilent_dso6014A import *


#######################
# Agilent model class #
#######################

class AgilentDSO7014A(AgilentDSO6014A):
    """ Agilent DSO6014A Oscilloscope model """

    # Instrument information
    brand = "AGILENT"
    model = "DSO7014A"


# Subscribing the new instrument to the lab-tool register
LabTool.add_oscilloscope(AgilentDSO7014A)
