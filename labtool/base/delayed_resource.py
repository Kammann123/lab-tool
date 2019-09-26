"""
DelayedResource is a class wrapping a common PyVisa Resource
adding a delay after each call of write(), read() and query().
"""

# python native modules
import time

# third-party modules
import pyvisa


class DelayedResource(object):
    """ PyVisa Resource wrapper with a delay time between function calls. """

    default_delay = 0

    def __init__(self, resource):
        self.resource = resource
        self.delay = DelayedResource.default_delay

    def set_delay(self, delay):
        self.delay = delay

    def write(self, *args, **kwargs):
        self.resource.write(*args, **kwargs)
        time.sleep(self.delay)

    def read(self, *args, **kwargs):
        return self.resource.read(*args, **kwargs)

    def query(self, *args, **kwargs):
        buffer = self.resource.query(*args, **kwargs)
        time.sleep(self.delay)
        return buffer

    def close(self):
        self.resource.close()
