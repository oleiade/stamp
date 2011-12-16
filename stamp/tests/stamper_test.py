#!/usr/bin/env python

import os
import unittest

from stamp import License, Stamper, constants

STAMPER_TEST_FILES_PREFIX = "stamper_test_file_"
APACHE_LICENSE_HEADER_CONTENT = """ Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

class TestStamper(unittest.TestCase):
    def __generate_test_files(self):
        """
        Generates test files on which license
        should be stamper.
        Returns a list of paths.
        """
        files_paths = []
        file_names = [
            "py_file.py",
            "c_file.c",
            "php_file.js",
        ]
        os.mkdir('/tmp/stamper_test')

        for counter, f in enumerate(file_names):
            path = self.test_files_dir + "/" + STAMPER_TEST_FILES_PREFIX + f
            f = open(path, 'w')
            f.close()
            files_paths.append(path)

        self.test_files_paths = files_paths

        return files_paths


    def __generate_test_license_file(self):
        license_file_path = "/tmp" + "/" + STAMPER_TEST_FILES_PREFIX + "apache_license"
        file_content = APACHE_LICENSE_HEADER_CONTENT

        f = open(license_file_path, 'w')
        f.write(file_content)
        f.close()

        self.test_license_file_path = license_file_path

        return license_file_path


    def __flush_test_files(self):
        for p in self.test_files_paths:
            f = open(p, 'w')
            f.flush()
            f.close()

        return


    def __remove_test_files(self):
        for p in self.test_files_paths:
            os.remove(p)

        return


    def assertListsList(self, lists_list):
        if lists_list and len(lists_list) > 0:
            for t in lists_list:
                self.assertIsInstance(t, list)


    def setUp(self):
        # Assigning function return value for memotechnic reasons
        self.test_files_dir = '/tmp/stamper_test'
        self.test_files_paths = self.__generate_test_files()
        self.test_license_file_path = self.__generate_test_license_file()

        self.license = License.License(self.test_license_file_path)
        self.inst = Stamper.Stamper(self.license)


    def test_apply_license_on_file(self):
        # getting the path of a file without shebang
        raw_path = self.test_files_paths[1]

        # dumping it's content in order to be able to compare
        # it after patching
        raw_file = open(raw_path, 'r').readlines()
        self.inst.apply_license(raw_path)
        licensed_file = open(raw_path, 'r').readlines()

        self.assertEqual(raw_file, [])
        self.assertIsInstance(licensed_file, list)
        self.assertNotEqual(licensed_file, [])

        # As selected test path has .c extension,
        # check the appliedlicense is a c commented one
        self.assertEqual(licensed_file[0:3], ['\n', '\n', '/*\n'])
        self.assertTrue(licensed_file[3].startswith('**'))


    def test_apply_license_on_path(self):
        # getting the path of files meant to be patched
        raw_paths = self.test_files_paths[1:]

        # dumping the files (empty) content, applying license to
        # the path their stored at. Retrieving their patched content.
        raw_files_content = [open(p, 'r').readlines() for p in raw_paths]
        self.inst.apply_license(self.test_files_dir)
        licensed_files_content = [open(f, 'r').readlines() for f in raw_paths]


        self.assertEqual(len(raw_files_content), len(licensed_files_content))
        i = 0
        # dumping it's content in order to be able to compare
        # it after patching
        while i < len(raw_files_content):
            raw_file = raw_files_content[i]
            licensed_file = licensed_files_content[i]
            self.assertEqual(raw_file, [])
            self.assertIsInstance(licensed_file, list)
            self.assertNotEqual(licensed_file, [])

            # As selected test path has .c extension,
            # check the appliedlicense is a c commented one
            self.assertEqual(licensed_file[0:3], ['\n', '\n', '/*\n'])
            self.assertTrue(licensed_file[3].startswith('**'))
            i += 1


    def tearDown(self):
        self.__flush_test_files()
        self.__remove_test_files()

        os.remove(self.test_license_file_path)
        os.rmdir(self.test_files_dir)

suite = unittest.TestLoader().loadTestsFromTestCase(TestStamper)
unittest.TextTestRunner(verbosity=2).run(suite)
