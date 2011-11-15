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

import utils

class Stamper:
    """ Class defining methods allowing to
    create a language specific commented license
    in order to apply it as a file header"""

    def __init__(self, license_inst):
        """Constructor"""
        self.license = license_inst


    def _get_folder_files(self, folder, exclude_dotted=True):
        """
        Given a folder, recursively retrieves contained files
        returns a list of tuples (file extension, file path).

        NB : Shall not be used independtly.

        folder                    String : path to retrieve files from.
        """
        listed_dirs = []

        for root, dirs, files in os.walk(folder):
            # If bool param is True, exclude dotted
            # dirs from computing.
            if exclude_dotted:
                dirs = utils.remove_dotted_path(dirs)
                files = utils.remove_dotted_path(files)
            for name in files:
                file_path = os.path.join(root, name)
                file_extension = utils.get_file_extension(file_path)

                # Stamper should not apply a header on file with
                # no language extension
                print "file %s : %s" % (name, self.license.is_valid_file_extension(file_extension))
                if self.license.is_valid_file_extension(file_extension):
                    listed_dirs.append((file_extension, file_path))

        return listed_dirs


    def _get_path_elements(self, path, exclude_dotted=True):
        """
        Recursively retrieves a given path files.
        returns a list of tuples (file extension, file path).
        If given path is a folder, returns get_folder_files result,
        else uses the given path file.

        path                    String : path to retrieve files from.
        exclude_dotted          Boolean : Wheter to ignore paths beggining
                                with a dot while walking dirs.
                                Ex : .git .svn .emacs
        """
        listed_elems = []

        if os.path.isdir(path):
            listed_elems = self._get_folder_files(path, exclude_dotted)
        else:
            file_path = utils.remove_dotted_path(path) if exclude_dotted \
                                                       else path
            if file_path:
                file_extension = utils.get_file_extension(file_path)
                if self.license.is_valid_file_extension(file_extension):
                    listed_elems = [(file_extension, file_path)]

        return(listed_elems)


    def _dump_file_content(self, path):
        """
        Method dumping a file content to a list

        path                    String : file to dump path
        """
        file_dump = []

        try:
            file_desc = open(path, 'r')
            file_dump = file_desc.readlines()
            file_dump.append("\n\n")
            file_desc.close()
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)

        return (file_dump)


    def write_header_to_file(self, dest_filename, header):
        """
        Method adding a given license list at the begining
        of a file

        dest_filename           String : candidate filename which license should
                                be applied to.
        header                  List : Formatted, license content to write
                                as a given destination file header.
        """
        try:
            file_dump =  self._dump_file_content(dest_filename)
            file_desc = open(dest_filename, 'w')
            file_desc.seek(0)
            file_desc.writelines(header + file_dump)
            file_desc.close()
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)


    def apply_license(self, path):
        """
        Applies a given license (class instance) to a given path.

        lic                     License : License class instance, should have
                                been initialized with one of your choice (apache, bsd, ...)
        path                    String : File or dir, License should apply to.
        """
        files_in_path = self._get_path_elements(path)

        for found_file in files_in_path:
            file_license = self.license.get_license_as(found_file[0])
            self.write_header_to_file(found_file[1], file_license)
