"""
LabTool module with a list of the available devices
"""

# python native modules
from enum import Enum
from time import sleep
from math import log10
from numpy import logspace

# third-party modules
import pyvisa
import xlwt

# labtool project modules
from labtool.oscilloscope.base.oscilloscope import Oscilloscope
from labtool.generator.base.generator import Generator

from labtool.oscilloscope.base.oscilloscope import Sources

from labtool.generator.base.generator import Waveform
from labtool.generator.base.generator import OutputLoad
from labtool.generator.base.generator import OutputMode
from labtool.oscilloscope.base.oscilloscope import AcquireMode

from labtool.base.instrument import InstrumentType
from labtool.base.instrument import Instrument


############################
# LabTool Enum Definitions #
############################

class BodeScale(Enum):
    Linear = "Linear"
    Log = "Log"


######################
# LabTool Exceptions #
######################

class DeviceNotFound(Exception):
    def __init__(self):
        super(DeviceNotFound, self).__init__("Could not find any device with the given instrument type."
                                             + " Verify the device connection or if the module has been imported.")


###################################
# LabTool static class definition #
###################################

class LabTool(object):
    """ LabTool backend logic methods. """

    # Available devices in the LabTool
    available_oscilloscopes = []
    available_generators = []
    resource_manager = None

    @staticmethod
    def get_manager() -> pyvisa.ResourceManager:
        if LabTool.resource_manager is None:
            LabTool.resource_manager = pyvisa.ResourceManager()
        return LabTool.resource_manager

    @staticmethod
    def close_manager():
        if LabTool.resource_manager is not None:
            LabTool.resource_manager.close()

    @staticmethod
    def to_enum(value: str, enum: Enum):
        for enum_value in enum:
            if enum_value.value == value:
                return enum_value

    @staticmethod
    def open_device_by_type(resource_type: InstrumentType) -> Instrument:
        """ Returns an Instrument interface to handle communication with the given type of instrument if connected.
        If no instruments are found, DeviceNotFound will be raised. """
        resources = LabTool.get_devices()
        for resource in resources:
            if LabTool.is_device_detected(resource) is resource_type:
                return LabTool.open_device_by_id(resource)

        raise DeviceNotFound

    @staticmethod
    def open_device_by_id(resource_id: str) -> Instrument:
        """ Returns an Instrument interface to handle communication with the given Device """
        resource_info = LabTool.get_device_information(resource_id)
        resource_type = LabTool.is_device_detected(resource_info)
        if resource_type is InstrumentType.Oscilloscope:
            for oscilloscope in LabTool.available_oscilloscopes:
                if oscilloscope.model == resource_info["model"]:
                    return oscilloscope(resource_id)
        elif resource_type is InstrumentType.Generator:
            for generator in LabTool.available_generators:
                if generator.model == resource_info["model"]:
                    return generator(resource_id)
        else:
            raise DeviceNotFound

    @staticmethod
    def is_device_detected(resource_information: dict) -> InstrumentType:
        """ Returns whether the Instrument has or not an interface installed with the LabTool packaged,
        in order to be used when connected.
        Returns -> InstrumentType if detected, None if was not detected. """

        # Veryfing if connected instrument is an oscilloscope
        for oscilloscope in LabTool.available_oscilloscopes:
            if oscilloscope.model == resource_information["model"]:
                return InstrumentType.Oscilloscope

        # Veryfing if connected instrument is a generator
        for generator in LabTool.available_generators:
            if generator.model == resource_information["model"]:
                return InstrumentType.Generator

        # Not detected...
        return None

    @staticmethod
    def get_devices() -> list:
        """ Returns a list of the currently connected devices, by returning their
        resource identifier internal to the PyVisa package. """
        resource_manager = LabTool.get_manager()
        resources = resource_manager.list_resources()
        return list(resources)

    @staticmethod
    def get_device_information(resource_id: str) -> list:
        """ Given a resource's identification returned by the PyVisa package ResourceManager,
            its information is returned, as follows:
            Returns -> {
                "brand": Instrument Brand,
                "model": Instrument Model,
                "series-number": Instrument Series Number
            }

            Note: It is being assumed that all instruments connected through VISA respond to a
            *IDN? command.
        """
        resource_manager = LabTool.get_manager()
        resource_interface = resource_manager.open_resource(resource_id)
        identification = resource_interface.query("*IDN?").split(",")
        resource_interface.close()

        return {
            "brand": identification[0].upper(),
            "model": identification[1].upper(),
            "series-number": identification[2].upper()
        }

    @staticmethod
    def add_oscilloscope(oscilloscope):
        """ Registers a new Oscilloscope Class """
        LabTool.available_oscilloscopes.append(oscilloscope)

    @staticmethod
    def add_generator(generator):
        """ Registers a new Generator Class """
        LabTool.available_generators.append(generator)

    @staticmethod
    def download_waveform(oscilloscope,
                          source,
                          waveform_format):
        """ Returns the waveform data from the given channel in the
        oscilloscope.
        Note: In this initial version of the LabTool,
        both preamble and data are returned so as to know what the
        oscilloscope is returning for those queries. """
        oscilloscope.digitize(source)
        oscilloscope.waveform_source(source)
        oscilloscope.waveform_format(waveform_format)
        oscilloscope.waveform_unsigned(True)
        oscilloscope.waveform_points(10000)

        preamble = oscilloscope.waveform_preamble()
        data = oscilloscope.waveform_data()

        return {
            "preamble": preamble,
            "data": data
        }
