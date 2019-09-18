"""
Sample_3: Testing an automatic identification of the device.
"""

# python native modules

# third-party modules

# labtool project modules
from labtool.oscilloscope.agilent.agilent_dso6014A import AgilentDSO6014
from labtool.generator.agilent.agilent_33220a import Agilent33220A

from labtool.base.instrument import InstrumentType
from labtool.base.instrument import Instrument

from labtool.tool import LabTool


if __name__ == "__main__":
    osc = LabTool.open_device(InstrumentType.Oscilloscope)
    gen = LabTool.open_device(InstrumentType.Generator)
