"""
Sample_0: Importing the pyVisa python package and creating an instance of ResourceManager to check whether
you have or not the NI-Visa Library installed. Remember, there are two standard options to run as libraries,
be sure you have one of them. (NI o pyvisa-py)
"""

# third-party modules
import pyvisa

from pyvisa.errors import *

if __name__ == "__main__":

    # Creating the ResourcesManager instance
    try:
        rm = pyvisa.ResourceManager()

        print("Library was loaded successfully!")
    except LibraryError:
        print("You do not have any Library installed, or at least PyVisa was unable to find it in the directory.")
    except OSError:
        print("There was a problem trying to load the library.")
