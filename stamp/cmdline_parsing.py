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


import argparse

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

    return parser


def compute_args(arg_parser):
    """
    Gets the arguments from the command line and checks
    they're passing a set of criterea.

    Example : the presence of the .lic extension
    attached to the license file name. (incoming feature)
    """
    args = arg_parser.parse_args()

    return args
