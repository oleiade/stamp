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

    def __init__(self):
        """Constructor"""
        pass

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
        listed_elems = []

        for root, dirs, files in os.walk(path):
            # If bool param is True, exclude dotted
            # dirs from computing.
            if exclude_dotted:
                for (counter, dir) in enumerate(dirs):
                    if dir.startswith('.'):
                        del dirs[counter - 1]
            for name in files:
                file_path = os.path.join(root, name)
                file_extension = self._getFileExtension(file_path)
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
#        for f in files_list:
#            self.files_content.append(self._dumpFileContent(f))


    def _writeHeaderToFile(self, dest_filename, headerToWrite):
        """
        Method adding a given license list at the begining
        of a file

        dest_filename           String : candidate filename which license should
                                be applied to.
        header                  String : Formatted, license content to write
                                as a given destination file header.
        """
        try:
            fileDump =  self._dumpFileContentToList(dest_filename)
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
        print files_in_path