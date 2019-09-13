"""
Sample_5: Testing export a csv file.
"""

# labtool project module
from labtool.tool import LabTool

if __name__ == "__main__":
    test = [
        {
            "frequency": 10,
            "input-vpp": 1,
            "output-vpp": 1,
            "bode-module": 10,
            "bode-phase": 45
        }
    ]

    LabTool.export_to_csv("test", test)
