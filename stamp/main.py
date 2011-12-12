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

from stamp import License
from stamp import Stamper
from stamp.cmdline_parsing import gen_arg_parser, compute_args

def main():
    """Main function"""
    arg_parser = gen_arg_parser()
    args = compute_args(arg_parser)

    if args.license_file:
        lic = License.License(args.license_file)
        stamper = Stamper.Stamper(lic)
        for path in args.paths:
            # as args.paths has been previously flagged with
            # it's elements type: path[0] = given path
            #                     path[1] = path kind (file or folder)
            stamper.apply_license(path[0], path_type=path[1],
                                  verbose=args.verbose)

    print "Done"
