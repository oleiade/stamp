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

class Stamper:
    """ Class defining methods allowing to
    create a language specific commented license
    in order to apply it as a file header"""

    def __init__(self, license_file):
        """Constructor"""
        self.__name = "fileLicenseType"
        self.__licenseContent = self.getLicenseFileContent(license_file)
        self.__licenseSize = self.getLicenseSize()
        self.__filesFuncs = {}
        self.__filesHeaders = {}
        self.initFileTypes()


    def initFileTypes(self):
        """Method initializing the corresponding method
        to apply on each file types"""
        self.__filesFuncs = {
            "c": self.cStyleComments,
            "h": self.cStyleComments,
            "cpp": self.cStyleComments,
            "hh": self.cStyleComments,
            "hpp": self.cStyleComments,
            "py": self.pyStyleComments,
            "pl": self.pyStyleComments,
            }


    def getTargetFilesList(self, path):
        """
        Recursively retrieves a given path files
        as a list

        path                    String : path to retrieve files from.
        """
        listedDirs = []

        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for name in files:
                    filename = os.path.join(root, name)
                    listedDirs.append(filename)
        else:
            listedDirs.append(path)
        return(listedDirs)


    def getLicenseFileContent(self, path):
        """
        Method returning the content of the license contained in
        file "filename" as a list. Yet it will raise an IOError exception

        path                    String : License file path
        """
        license_content = None

        try:
            fd = open(path, 'r')
            license_content = fd.readlines()
            fd.close()
        except IOError as (errno, strerror):
        # Pep8 incompatible Multi-line try/except
        # taken from python doc
        # (http://docs.python.org/tutorial/errors.html#handling-exceptions)
            print "I/O error({0}): {1}".format(errno, strerror)

        return (license_content)


    def getLicenseSize(self):
        """Returns the license file size"""
        licenseSize = 0

        for elem in self.__licenseContent:
            licenseSize += len(elem)
        return licenseSize


    def dumpFileContentToList(self, path):
        """
        Method dumping a file content to a list

        path                    String : file to dump path
        """
        try:
            fd = open(path, 'r')
            fileDump = fd.readlines()
            fileDump.append("\n\n")
            fd.close()
            return (fileDump)
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)


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
            fileDump =  self.dumpFileContentToList(dest_filename)
            fd = open(dest_filename, 'w')
            fd.seek(0)
            fd.writelines(headerToWrite + fileDump)
            fd.close()
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)


    def applyLicenseToFile(self, dest_filename):
        """
        Adds the given/found license into a given file

        dest_filename           String : candidate filename which license should
                                be applied to.
        """
        headerToWrite = ""
        fileDescription = dest_filename.split('.')
        fileType = str(fileDescription[-1])

        if fileType in self.__filesFuncs:
            if fileType in self.__filesHeaders:
                headerToWrite = self.__filesHeaders[fileType]
            else:
                headerToWrite = self.__filesFuncs[fileType](self.__licenseContent)
                self.__filesHeaders[fileType] = headerToWrite
            self.writeHeaderToFile(dest_filename, headerToWrite)


    def cStyleComments(self, licenseContent):
        """
        Method formating a given license content list,
        to C Style language commented output

        licenseContent          List : Retrieved license content from file
        """
        newLicense = []
        newLicense.insert(0, "/*\n")

        for line in licenseContent:
            newLicense.append("** " + line)
        newLicense.append("*/\n\n")
        return (newLicense)


    def pyStyleComments(self, licenseContent):
        """
        Method formating a given license content list,
        to Python Style language commented output

        licenseContent          List : Retrieved license content from file
        """
        newLicense = []

        for line in licenseContent:
            newLicense.append("# " + line)
        newLicense.append("\n\n")
        return (newLicense)


    def applyLicenseToFiles(self, path):
        """
        Applies a given/found license as
        a header to recursively found files in path

        path                    String : Path where to seek for files
        """
        files = self.getTargetFilesList(path)

        for f in files:
            self.applyLicenseToFile(f)






