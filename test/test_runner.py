"""
    Discovers all tests and runs them. Assumes that initially the working directory is test and source is not known
    in the sys path.
"""

import sys
import os
import unittest

if __name__ == '__main__':

    # add source directory to path if needed
    source_directory = os.path.abspath(os.path.join('..', 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    loader = unittest.defaultTestLoader

    tests = loader.discover('.')

    runner = unittest.TextTestRunner()

    runner.run(tests)