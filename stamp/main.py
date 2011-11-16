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

from License import License
from Stamper import Stamper

def main():
    """Main function"""
    if (len(sys.argv) >= 3):
        lic = License(sys.argv[-1])
        stamper = Stamper(lic)
        paths = sys.argv[1:-1]
        for path in paths:
            stamper.apply_license(path)
    else:
        print """Usage: ./license-applier.py <file/dir 1\
        ... file/dir n> license_file"""

