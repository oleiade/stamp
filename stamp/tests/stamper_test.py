#!/usr/bin/env python

import os
import unittest

from stamp import License, Stamper, constants


class TestStamper(unittest.TestCase):
    """

    """
    def assertTuplesList(self, tuples_list):
        if tuples_list and len(tuples_list) > 0:
            for t in tuples_list:
                self.assertIsInstance(t, tuple)

    def setUp(self):
        self.test_content_path = os.path.join(os.path.dirname(__file__), 'test_content')
        test_license_path = os.path.join(self.test_content_path, 'valid_test_license_file.txt')

        self.license = License.License(test_license_path)
        self.inst = Stamper.Stamper(self.license)


    def test_get_folder_files(self):
        test_folder = os.path.join(self.test_content_path, 'test_dir')
        folder_total_files = 5
        folder_dotted_files = 3
        folder_nodotted_files = 2
        folder_dotted_ext_files = 1

        nodotted_folder_content = self.inst._get_folder_files(test_folder, exclude_dotted=True)
        dotted_folder_content = self.inst._get_folder_files(test_folder, exclude_dotted=False)

        self.assertIsInstance(nodotted_folder_content, list)
        self.assertIsInstance(dotted_folder_content, list)
        self.assertTuplesList(nodotted_folder_content)
        self.assertTuplesList(dotted_folder_content)

        self.assertEqual(len(nodotted_folder_content), folder_total_files - folder_dotted_files)  # 2 == 2
        # Only dotted files using an extension should pass
        self.assertEqual(len(dotted_folder_content), folder_nodotted_files + folder_dotted_ext_files)  # 3 == 3


    def tearDown(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(TestStamper)
unittest.TextTestRunner(verbosity=2).run(suite)

