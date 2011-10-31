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


LANG_EXTENSIONS = {
    "c": ["c", "cc", "cpp", "h", "hh", "hpp"],
    "c++": ["c", "cc", "cpp", "h", "hh", "hpp"],
    "python": ["py"],
    "perl": ["pl"],
    "php": ["php"],
    "elisp": ["el"],
    "haskell": ["hl"],
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
        self.LANG_COMMENT_FAMILY = {
            "stars": ["c", "c++", "js", "php"],
            "sharps": ["python", "perl"],
            "semicolon": ["elisp"]
            }

        # Tuple should always have three elems,
        # a prefix, content comment, suffix.
        self.LANG_COMMENT_STYLE = {
            "stars": ('/*', '**', '*/'),
            "sharps": ('', '#', ''),
            "semicolon": ('', ';;', ''),
            }

        self.extensions = [item for sublist in LANG_EXTENSIONS.values for item in sublist]

        self.license_file = license_file
        self.content = self._getLicenseFileContent()
        self.size = self._getLicenseSize()

        # Instance attr which intends to dump generated
        # licenses in a list.
        self.buffered_licenses = {}


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


    def is_valid_file_extension(file_extension):
        """
        Checks whether given file extension is managed
        or not by License class.

        file_extension          String : file extension (py, c, pl, and so on...)
        """
        if file_extension and isinstance(file_extension, str):
            return True if (file_extension in self.extensions) else False
        return False

    def as_dict(self):
        """
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
        if lang in LANG_EXTENSIONS.keys():
            for key, value in self.LANG_COMMENT_FAMILY.items():
                if lang in value:
                    comment_pattern = self.LANG_COMMENT_STYLE[key]
        else:
            raise KeyError("%s language name does not seem to be present in languages extensions dict" % (lang))

        # Updating license content in order to comment it out
        # using computed comment pattern
        formatted_license.insert(0, comment_pattern[0] + "\n")
        for line in self.content:
            formatted_license.append(comment_pattern[1] + " " + line)
        formatted_license.append(comment_pattern[2] + "\n")

        return (formatted_license)


    def get_license_as(self, lang):
        """
        Proxy method which retrieves formatted license content
        from instance buffer licenses list if already computed.
        formats it and adds it to buffer if not.

        lang            String : Language name to use comment pattern
                        from.
        """
        if lang.lower() in self.buffered_licenses.keys():
            return self.buffered_licenses[lang]
        else:
            self.buffered_licenses[lang] = self.format_as(lang)

        return self.buffered_licenses[lang]
