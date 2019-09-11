"""
Oscilloscope base class. It contains the base methods that should be defined
or implemented by any child class defining a specific oscilloscope model.
"""

# python native modules
from abc import ABC


# labtool project modules
from labtool.instrument import Instrument


class Oscilloscope(Instrument, ABC):
    """ Oscilloscope Base Class.
    When inheriting to define a child class, static parameters are needed
    to be recognized by the labtool """

    # Oscilloscope static parameters
    brand = "OscilloscopeBrand"
    model = "OscilloscopeModel"

