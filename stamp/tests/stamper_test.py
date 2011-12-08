#!/usr/bin/env python

import os
import unittest

from stamp.tests.utilities import assertListsList
from stamp import License, Stamper, constants


class TestStamper(unittest.TestCase):
    """

    """
    def setUp(self):
        self.test_content_path = os.path.join(os.path.dirname(__file__), 'test_content')
        self.test_license_path = os.path.join(self.test_content_path, 'valid_test_license_file.txt')

        self.license = License.License(self.test_license_path)
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
        self.assertListsList(nodotted_folder_content)
        self.assertListsList(dotted_folder_content)

        self.assertEqual(len(nodotted_folder_content), folder_total_files - folder_dotted_files)  # 2 == 2
        # Only dotted files using an extension should pass
        self.assertEqual(len(dotted_folder_content), folder_nodotted_files + folder_dotted_ext_files)  # 3 == 3


    def test_get_path_file_descriptor(self):
        i = 0
        mode = 'r'

        while i < 15:
            self.inst._get_fd_from_path(self.test_license_path, mode)
            i += 1

        # Though we asked multiple file descriptor, the buffer
        # should only contain one, as we unduplicate paths using
        # dictionnary.
        self.assertEqual(len(self.inst.fd_buffer), 1)
        for f in self.inst.fd_buffer.values():
            self.assertIsInstance(f, file)
            self.assertFalse(f.closed)
            self.assertEqual(f.mode, mode)


    def test_clear_fd_buffers(self):
        mode = 'r'
        i = 0

        while i < 15:
            self.inst._get_fd_from_path(self.test_license_path, mode)
            i += 15

        fd_buffers_dump = self.inst.fd_buffer
        self.assertEqual(len(fd_buffers_dump), 1)

        self.inst._clear_fd_buffers()
        for fd in fd_buffers_dump.values():
            self.assertTrue(fd.closed)
        self.assertEqual(self.inst.fd_buffer, {})


    def tearDown(self):
        self.inst.fd_buffers = {}

suite = unittest.TestLoader().loadTestsFromTestCase(TestStamper)
unittest.TextTestRunner(verbosity=2).run(suite)
