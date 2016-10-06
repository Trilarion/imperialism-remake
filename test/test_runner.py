"""
    Discovers all tests and runs them.
"""

import unittest

if __name__ == '__main__':

    loader = unittest.defaultTestLoader

    tests = loader.discover('.')

    runner = unittest.TextTestRunner()

    runner.run(tests)