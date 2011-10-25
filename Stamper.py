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

LANGUAGES = {
    "c": ["c", "cc", "cpp", "h", "hh", "hpp"],
    "c++": ["c", "cc", "cpp", "h", "hh", "hpp"],
    "python": ["py"],
    "perl": ["pl"],
    "php": ["php"],
    "elisp": ["el"],
    "haskell": ["hl"]
    "js": ["js"],
    }


class License:
    """
    Class which intends to manage a license file I/O
    operations. Can be used in order to retrieve it's
    (license file)content, output it as various data
    structures.
    """

    def __init__(self, license_file):
        LANG_COMMENT_FAMILY = {
            "stars": ["c", "c++", "js", "php"],
            "sharps": ["python", "perl"],
            "semicolon": ["elisp"]
            }

        # Tuple should always have three elems,
        # a prefix, content comment, suffix.
        LANG_COMMENT_STYLE = {
            "stars": ('/*', '**', '*/'),
            "shaprs": ('', '#', ''),
            "semicolon": ('', ';;', ''),
            }

        self.license_file = license_file
        self.content = self._getLicenseFileContent()
        self.size = self._getLicenseSize()

        return comment_style


    def format_as(self, lang="c"):
        """
        Method formating license content list using a given language
        comment pattern.

        lang            String : Language name to use comment pattern
                        from.
        """
        comment_pattern = None
        formatted_license = []

        # Retrieving given language comment pattern
        for key, value in self.LANG_COMMENT_FAMILY.items():
            if lang in value:
                comment_pattern = LANG_COMMENT_STYLE[key]

        # Updating license content in order to comment it out
        # using computed comment pattern
        formatted_license.insert(0, comment_pattern[0] + "\n")
        for line in self.content:
            formatted_license.append(comment_pattern[1] + " " + line)
        formatted_license.append(comment_pattern[2] + "\n")

        return (formatted_license)


    def _getLicenseFileContent(self):
        """
        Retrieves the content of the license file as a list.
        Yet it will raise an IOError exception
        """
        content = None

        try:
            fd = open(self.license_file, 'r')
            content = fd.readlines()
            fd.close()
        except IOError as (errno, strerror):
        # Pep8 incompatible Multi-line try/except
        # taken from python doc
        # (http://docs.python.org/tutorial/errors.html#handling-exceptions)
            print "I/O error({0}): {1}".format(errno, strerror)

        return (content)


    def _getLicenseSize(self):
        """Returns the license content size"""
        size = 0

        for elem in self.content:
            size += len(elem)

        return size


    def as_dict(self):
        """
        """
        return {
            "content": self.content,
            "size": self.size,
            }


class Stamper:
    """ Class defining methods allowing to
    create a language specific commented license
    in order to apply it as a file header"""

    def __init__(self):
        """Constructor"""
        pass


    def _getFilesList(self, path):
        """
        Recursively retrieves a given path files
        as a list

        path                    String : path to retrieve files from.
        """
        listed_elems = []

        for root, dirs, files in os.walk(path):
            for name in files:
                filename = os.path.join(root, name)
                listed_elem.append(filename)

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
        self
