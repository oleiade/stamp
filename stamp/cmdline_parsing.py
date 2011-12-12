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
import argparse

from stamp import utils
from stamp.constants import OPTION_TYPE_FILE, OPTION_TYPE_FOLDER

def gen_arg_parser():
    """
    Generates the application command line
    arguments parser.

    returns a argparse.ArgumentParser class instance.
    """
    parser = argparse.ArgumentParser(description="Applies a given license to files/folders")
    parser.add_argument('license_file', metavar='License file', type=str, action='store',
                        help='Path to the license content file to apply on given files')
    parser.add_argument('paths', metavar='File/Folder', type=str, nargs='+',
                        help='Files or folder to recursively add license to')

    parser.add_argument('-v', '--verbose', action='append_const', const=1)

    return parser


def assert_license_file_format(args):
    """
    Assert param given license file has the .lic extension.
    """
    passes = True
    error_message = None
    file_ext = utils.get_file_extension(args.license_file)

    if file_ext != 'lic':
        passes = False
        error_message = "Error : Only .lic license files format is valid"

    return passes, error_message


def markup_options_file_folder_types(args):
    """
    Returns files and folders to patch taken from
    command line options as a list of tuples containing
    each the file/folder path, and it's type macro.
    """
    new_paths = []

    for p in args.paths:
        # Checking if path is a dir or not.
        # might be a more elegant way to do this
        # (with less system calls)
        path_type = OPTION_TYPE_FOLDER if os.path.isdir(p) else OPTION_TYPE_FILE
        new_paths.append((p, path_type))

    args.paths = new_paths

    return args

def compute_args(arg_parser):
    """
    Gets the arguments from the command line and checks
    they're passing a set of criterea.

    Example : the presence of the .lic extension
    attached to the license file name. (incoming feature)
    """
    args = arg_parser.parse_args()
    assertions = [assert_license_file_format]

    # Mark files/folders retrieved from command
    # with their type.
    markup_options_file_folder_types(args)

    for assertion in assertions:
        passes, error_msg = assertion(args)
        if not passes:
            arg_parser.error(error_msg)
            break

    return args
