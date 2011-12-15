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
            "php_file.php",
        ]

        for counter, f in enumerate(file_names):
            path = "/tmp" + "/" + STAMPER_TEST_FILES_PREFIX + f
            f = open(path, 'w')

            if counter == 0:
                f.write("#!/usr/bin/env python\n\n This is a shebanged test file content")
            else:
                f.write("This is a test file content")

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


    def assertListsList(self, lists_list):
        if lists_list and len(lists_list) > 0:
            for t in lists_list:
                self.assertIsInstance(t, list)


    def setUp(self):
        # Assigning function return value for memotechnic reasons
        self.test_files_paths = self.__generate_test_files()
        self.test_license_file_path = self.__generate_test_license_file()

        self.license = License.License(self.test_license_file_path)
        self.inst = Stamper.Stamper(self.license)


    def test_apply_license(self):
        pass


    def tearDown(self):
        self.__flush_test_files()

suite = unittest.TestLoader().loadTestsFromTestCase(TestStamper)
unittest.TextTestRunner(verbosity=2).run(suite)
