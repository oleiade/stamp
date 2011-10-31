#!/usr/bin/env python

# Copyright 2010 Theo Crevon
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys

import License


class Stamper:
    """ Class defining methods allowing to
    create a language specific commented license
    in order to apply it as a file header"""

    def __init__(self, license_inst):
        """Constructor"""
        self.license = license_inst

    def _getFileExtension(self, filepath):
        """
        Extracts extension from file path.
        """
        file_name, file_extension = os.path.splitext(filepath)

        # return file_extension without it's
        # starting point
        return file_extension[1:]

    def _getFilesList(self, path, exclude_dotted=True):
        """
        Recursively retrieves a given path files
        as a list of tuples (file extension, file path).

        path                    String : path to retrieve files from.
        exclude_dotted          Boolean : Wheter to ignore paths beggining
                                with a dot while walking dirs.
                                Ex : .git .svn .emacs
        """
        def remove_dotted_dirs_from_list(walked_list):
            """
            Nested subfunction which removes dirs and files
            begginingg with dots from a given list, which could
            have been yielded by os.walk for example.

            walked_list         List : path list where to search and remove
                                those who begins with a dot.
            """
            for (counter, elem) in enumerate(walked_list):
                if elem.startswith('.'):
                    del walked_list[counter - 1]

            return walked_list

        listed_elems = []

        for root, dirs, files in os.walk(path):
            # If bool param is True, exclude dotted
            # dirs from computing.
            if exclude_dotted:
                dirs = remove_dotted_dirs_from_list(dirs)
                files = remove_dotted_dirs_from_list(files)
            for name in files:
                file_path = os.path.join(root, name)
                file_extension = self._getFileExtension(file_path)

                # Stamper should not apply a header on file with
                # no language extension
                if self.license.is_valid_file_extension(file_extension):
                    listed_elems.append((file_extension, file_path))

        return(listed_elems)


    def _dumpFileContent(self, path):
        """
        Method dumping a file content to a list

        path                    String : file to dump path
        """
        fileDump = []

        try:
            fd = open(path, 'r')
            fileDump = fd.readlines()
            fileDump.append("\n\n")
            fd.close()
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)

        return (fileDump)


    def _dumpFiles(self, files_list):
        """

        """
        for f in files_list:
            self.files_content.append(self._dumpFileContent(f))


    def writeHeaderToFile(self, dest_filename, headerToWrite):
        """
        Method adding a given license list at the begining
        of a file

        dest_filename           String : candidate filename which license should
                                be applied to.
        header                  String : Formatted, license content to write
                                as a given destination file header.
        """
        try:
            fileDump =  self._dumpFileContent(dest_filename)
            fd = open(dest_filename, 'w')
            fd.seek(0)
            fd.writelines(headerToWrite + fileDump)
            fd.close()
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)


    def applyLicense(self, license, path):
        """
        """
        files_in_path = self._getFilesList(path)

        for f in files_in_path:
            file_license = self.license.get_license_as(f[0])
            self.writeHeaderToFile(f[1], file_license)
