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
    """
    Class defining methods allowing to
    create a language specific commented license
    in order to apply it as a file header
    """

    def __init__(self, license_inst):
        """Constructor"""
        self.MAX_CONCURRENT_FD = 128
        self.PATH_CHUNKS_SIZE = 128

        self.license = license_inst
        self.fd_buffer = {}


    def _has_shebang(self, file_content):
        """
        Checks if a file, given as a list, contains
        a shebang instruction as it's first line.
        If it does, returns the file first line in order
        to reinsert it in the processed files later. Else
        it will return None.

        file_content            List : file to test content list
        """
        first_line = str(file_content[0]).strip()

        if first_line[0:3] == "#!/":
            return first_line
        else:
            return None


    def _get_folder_files(self, folder, exclude_dotted=True):
        """
        Given a folder, recursively retrieves contained files
        returns a list of lists ([file extension, file path]).

        NB : Shall not be used independtly.

        folder                  String : path to retrieve files from.
        exclude_dotted          Bool : Wheter to ignore paths beggining
                                with a dot while walking dirs.
                                Ex : .git .svn .emacs
        """
        listed_dirs = []

        for root, dirs, files in os.walk(folder):
            # If bool param is True, exclude dotted
            # dirs from computing.
            if exclude_dotted:
                dirs = utils.remove_dotted_path_elements(dirs)
                files = utils.remove_dotted_path_elements(files)
            for name in files:
                file_path = os.path.join(root, name)
                file_extension = utils.get_file_extension(file_path)

                # Stamper should not apply a header on file with
                # no language extension
                if self.license.is_valid_file_extension(file_extension):
                    listed_dirs.append([file_extension, file_path])

        return listed_dirs


    def _get_path_elements(self, path, exclude_dotted=True):
        """
        Recursively retrieves a path files.
        returns a list of lists -- [file extension, file path]
        If path is a folder, returns get_folder_files result,
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
            file_path = utils.remove_dotted_path_elements(path) if exclude_dotted \
                                                       else path
            if file_path:
                file_extension = utils.get_file_extension(file_path)
                if self.license.is_valid_file_extension(file_extension):
                    listed_elems = [[file_extension, file_path]]

        return(listed_elems)


    def _dump_file_content(self, file_descriptor):
        """
        Method dumping a file content to a list.

        file_descriptor         File : file descriptor to dump
                                content from.
        """
        file_dump = []

        try:
            file_dump = file_descriptor.readlines()
            file_dump.append("\n\n")
            # using fd buffer, always seek(0) after each operation.
            file_descriptor.seek(0)
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)

        return file_dump


    def _get_fd_from_path(self, path, mode="r+"):
        """
        Opens a file_descriptor from a path, using
        with given mode. Adds it to the stamper class
        file descriptor buffer.

        path                    String : file path to buffer a file
                                descriptor from.
        mode                    String : file path descriptor mode to use.
        """
        # Checking there is a free slot in the fd buffer
        if len(self.fd_buffer) < self.MAX_CONCURRENT_FD:
            try:
                file_desc = open(path, mode)
                self.fd_buffer[path] = file_desc
            except IOError as (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
        else:
            return False

        return True


    def buffer_file_descriptors(self, paths_list, mode):
        """
        Recursively open file descriptor and add
        the paths pointed by the paths_list
        to the object file descriptor buffer.

        paths_list              List : paths, that should be opened
                                as a file descriptor and putted into
                                the stamper fd buffer.
        mode                    string : file descriptor opening mode
                                that should be used.
        """
        for p in paths_list:
            self._get_fd_from_path(p, mode=mode)

        return


    def _clear_fd_buffers(self):
        """
        Walks through the stamper object file descriptor
        buffer, close every found fd, and clears the
        stack.
        """
        for fd in self.fd_buffer.values():
            try:
                fd.close()
            except IOError as (errno, strerror):
                print "I/O error({0}: {1}".format(errno.strerror)

        self.fd_buffer = {}

        return


    def write_header_to_file(self, file_descriptor, header):
        """
        Method adding a license content at the begining
        of a file

        file_descriptor         File : open file descriptor where to write
                                license header.
        header                  List : Formatted, license content to write
                                as a given destination file header.
        """
        try:
            file_dump =  self._dump_file_content(file_descriptor)
            # only apply header if

            shebang = self._has_shebang(file_dump)
            # Applying license only if file has a shebang
            if shebang:
                file_dump = file_dump[1:]

            file_descriptor.writelines([shebang or "" + '\n\n'] + header + file_dump)
            # using fd buffer, always seek(0) after each operation.
            file_descriptor.seek(0)
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)


    def apply_license(self, path, verbose=False):
        """
        Applies a given license (class instance) to a given path.

        path                    String : File or dir, License should apply to.
        verbose                 Bool : Whether should display it's actions on
                                stdout or not.
        """
        files_in_path = self._get_path_elements(path)

        for chunk in utils.chunker(files_in_path, self.PATH_CHUNKS_SIZE):
            paths = [x[1] for x in chunk]  # Extract file paths
            self.buffer_file_descriptors(paths, mode='r+')

            for elem in chunk:
                # apply license using file extension
                file_license = self.license.get_license_as(elem[0])
                # retrieve the buffered file descriptor from path
                self.write_header_to_file(self.fd_buffer[elem[1]], file_license)
                if verbose :
                    print "Stamping: %s" % found_file[1]
            self._clear_fd_buffers()

        return
