#!/usr/bin/env python

import os
import unittest

import License, Stamper, constants

class TestStamper(unittest.TestCase):
    """

    """
    def setUp(self):
        self.test_content_path = os.path.join(os.path.dirname(__file__), 'test_content')
        test_license_path = os.path.join(self.test_content_path, 'valid_test_license_file.txt')

        self.license = License.License(test_license_path)
        self.inst = Stamper.Stamper(self.license)


    def test_get_folder_files(self):
        test_folder = os.path.join(self.test_content_path, 'test_dir')
        folder_total_files = 4
        folder_dotted_files = 2

        nodotted_folder_content = self.inst._get_folder_files(test_folder)
        dotted_folder_content = self.inst._get_folder_files(test_folder, exclude_dotted=False)

        self.assertEqual(len(nodotted_folder_content), folder_total_files - folder_dotted_files)
        self.assertEqual(len(dotted_folder_content), folder_total_files)


    def tearDown(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(TestStamper)
unittest.TextTestRunner(verbosity=2).run(suite)

