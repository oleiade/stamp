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

import constants

class License:
    """
    Class which intends to manage a license file I/O
    operations. Can be used in order to retrieve it's
    (license file)content, output it as various data
    structures.
    """

    def __init__(self, license_file):
        """Constructor"""
        self.ext = [item for subl in constants.LANG_EXTENSIONS.values()\
                         for item in subl]
        self.license_file = license_file
        self.content = self._get_license_file_content()
        self.size = self._get_license_size()

        # Instance attr which intends to dump generated
        # licenses in a list.
        self.buffered_licenses = {}


    def _get_license_file_content(self):
        """
        Retrieves the content of the license file as a list.
        Yet it will raise an IOError exception
        """
        content = None

        try:
            file_desc = open(self.license_file, 'r')
            content = file_desc.readlines()
            file_desc.close()
        except IOError as (errno, strerror):
        # Pep8 incompatible Multi-line try/except
        # taken from python doc
        # (http://docs.python.org/tutorial/errors.html#handling-exceptions)
            print "I/O error({0}): {1}".format(errno, strerror)

        return (content)


    def _get_license_size(self):
        """Returns the license content size"""
        size = 0

        for elem in self.content:
            size += len(elem)

        return size


    def is_valid_file_extension(self, file_extension):
        """
        Checks whether given file extension is managed
        or not by License class.

        file_extension          String : file extension (py, c, pl, and so on...)
        """
        if file_extension and isinstance(file_extension, str):
            return True if (file_extension.lower() in self.ext) else False
        return False


    def get_lang_from_extension(self, extension):
        """
        Returns the language matching to the given extension
        in LANG_EXTENSIONS or fail raising an IndexError.

        extension               String : extension to match with
                                LANG_EXTENSIONS languages.
        """
        for key, value in constants.LANG_EXTENSIONS.items():
            if extension.lower() in value:
                return key.lower()

        raise IndexError("""Could not find any language matching \
                            with the extension...""")

    def as_dict(self):
        """
        Returns a dict output of License class
        attributes values.
        """
        return {
            "content": self.content,
            "size": self.size,
            }


    def format_as(self, lang):
        """
        Method formating license content list using a given language
        comment pattern.

        lang            String : Language name to use comment pattern
                        from.
        """
        comment_pattern = None
        formatted_license = []
        lang = lang.lower()

        # Retrieving given language comment pattern
        if lang in constants.LANG_EXTENSIONS.keys():
            for key, value in constants.LANG_COMMENT_FAMILY.items():
                if lang in value:
                    comment_pattern = constants.LANG_COMMENT_STYLE[key]
        else:
            raise KeyError("""%s language name does not seem to be present \
                              in languages extensions dict""" % (lang))

        # Updating license content in order to comment it out
        # using computed comment pattern
        formatted_license.insert(0, comment_pattern[0] + "\n")
        for line in self.content:
            formatted_license.append(comment_pattern[1] + " " + line)
        formatted_license.append(comment_pattern[2] + "\n")

        return (formatted_license)


    def get_license_as(self, extension):
        """
        Proxy method which retrieves formatted license content
        from instance buffer licenses list if already computed.
        formats it and adds it to buffer if not.

        extension       String : extension to get formatted license
                        from.
        """
        if extension.lower() in self.buffered_licenses.keys():
            return self.buffered_licenses[extension]
        else:
            self.buffered_licenses[extension.lower()] = self.format_as(self.get_lang_from_extension(extension))

        return self.buffered_licenses[extension.lower()]
