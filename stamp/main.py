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


import sys
import argparse

from stamp import License
from stamp import Stamper


def gen_arg_parser():
    """
    Generates the application command line
    arguments parser.

    returns a argparse.ArgumentParser class instance.
    """
    parser = argparse.ArgumentParser(description="Applies a given license to files/folders")
    parser.add_argument('paths', metavar='File/Folder', type=str, nargs='+',
                        help='Files or folder to recursively add license to')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--license-file', dest="license_file",
                        type=str, help='Specify a license file to use, instead of any known pattern')
    # Will be used when License inherited classes will implement common
    # licenses existing paterns.
    group.add_argument('-p', '--license-pattern', dest="license_pattern",
                       type=str, help='Which license pattern to use')

    return parser


def main():
    """Main function"""
    arg_parser = gen_arg_parser()
    args = arg_parser.parse_args()

    if args.license_file:
        lic = License.License(args.license_file)
        stamper = Stamper.Stamper(lic)
        for path in args.paths:
            stamper.apply_license(path)
#    else:
#        print """Usage: ./license-applier.py <file/dir 1\
#        ... file/dir n> license_file"""
