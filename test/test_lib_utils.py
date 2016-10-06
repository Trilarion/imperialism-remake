"""
    Tests lib/utils
"""

import os
import unittest
import lib.utils as utils

class TestYAML(unittest.TestCase):

    def test_write_read(self):
        value = {
            "One": [2, 3, 'Four', None],
            2: ("Cat", "Dog")
        }
        temp_file = 'temporary_file'
        if os.path.exists(temp_file):
            raise RuntimeError('temporary file already existing')
        utils.write_as_yaml(temp_file, value)
        copy = utils.read_as_yaml(temp_file)
        os.remove(temp_file)
        self.assertEqual(value, copy)

if __name__ == '__main__':
    unittest.main()