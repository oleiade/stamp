#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
# 
#  http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


#!/usr/bin/env python

import os
import sys

class                   fileLicenseType:
    """ Class defining methods allowing to
    create a language specific commented license
    in order to apply it as a file header"""

    def                 __init__(self, license_file):
        """ Constructor """
        self.__name = "fileLicenseType"
        self.__licenseContent = self.getLicenseContent(license_file)
        self.__licenseSize = self.getLicenseSize()
        self.__filesFuncs = {}
        self.__filesHeaders = {}
        self.initFileTypes()

    def                 initFileTypes(self):
        """ Method initializing the corresponding method
        to apply on each file types """
        self.__filesFuncs = {
            "c": self.cstyleComments,
            "h": self.cstyleComments,
            "cpp": self.cstyleComments,
            "hh": self.cstyleComments,
            "hpp": self.cstyleComments,
            "py": self.pystyleComments,
            "pl": self.pystyleComments,
            }

    def                 getFilesList(self, path):
        """ Method returning a list of files contained in pointed dir
        parameter and it's subdirectories"""
        listedDirs = []

        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for name in files:
                    filename = os.path.join(root, name)
                    listedDirs.append(filename)
        else:
            listedDirs.append(path)
        return(listedDirs)

    def                 getLicenseContent(self, license_file):
        """ Method returning the content of the license contained in
        file "filename" as a list. Yet it will raise an IOError exception"""
        try:
            fd = open(license_file, 'r')
            licenseContent = fd.readlines()
            fd.close()
            return (licenseContent)
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)

    def                 getLicenseSize(self):
        licenseSize = 0

        for elem in self.__licenseContent:
            licenseSize += len(elem)
        return licenseSize

    def                 dumpFileToList(self, filename):
        """ Method dumping a file content to a list"""
        try:
            fd = open(filename, 'r')
            fileDump = fd.readlines()
            fileDump.append("\n\n")
            fd.close()
            return (fileDump)
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)

    def                 writeHeaderToFile(self, dest_file, headerToWrite):
        """ Method adding a given license list at the begining
        of a file """
        try:
            fileDump =  self.dumpFileToList(dest_file)
            fd = open(dest_file, 'w')
            fd.seek(0)
            fd.writelines(headerToWrite + fileDump)
            fd.close()
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)

    def                 applyLicenseToFile(self, dest_file):
        headerToWrite = ""
        fileDescription = dest_file.split('.')
        fileType = str(fileDescription[-1])

        if fileType in self.__filesFuncs:
            if fileType in self.__filesHeaders:
                headerToWrite = self.__filesHeaders[fileType]
            else:
                headerToWrite = self.__filesFuncs[fileType](self.__licenseContent)
                self.__filesHeaders[fileType] = headerToWrite
            self.writeHeaderToFile(dest_file, headerToWrite)

    def                 cstyleComments(self, licenseContent):
        """ Method formating a given license content list,
        to C Style language commented output """
        newLicense = []
        newLicense.insert(0, "/*\n")

        for line in licenseContent:
            newLicense.append("** " + line)
        newLicense.append("*/\n\n")
        return (newLicense)

    def                 pystyleComments(self, licenseContent):
        """ Method formating a given license content list,
        to Python Style language commented output """
        newLicense = []

        for line in licenseContent:
            newLicense.append("# " + line)
        newLicense.append("\n\n")
        return (newLicense)

    def                 applyLicense(self, path):
        files = self.getFilesList(path)

        for f in files:
            self.applyLicenseToFile(f)


def                     main():
    argv = sys.argv
    argc = len(argv)

    if (argc >= 3):
        fileLicenseInstance = fileLicenseType(sys.argv[-1])
        elemsToMod = sys.argv[1:-1]
        for elem in elemsToMod:
            fileLicenseInstance.applyLicense(elem)
    else:
        print "Usage: ./license-applier.py <file/dir 1 ... file/dir n> license_file"

if __name__ == "__main__":
    main()


