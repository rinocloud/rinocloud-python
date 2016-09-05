import os
import unittest

from .test_rinocloud import RinocloudObjectTest, RinocloudCollectionTest

def all():
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest.defaultTestLoader.discover(path)
