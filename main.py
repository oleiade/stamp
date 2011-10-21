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
from Stamper import License, Stamper

def                     main():
    argv = sys.argv
    argc = len(argv)
    print argv, argc

    if (argc >= 3):
        license = License(sys.argv[-1])
        licenseMan = Stamper(license)
        elemsToMod = sys.argv[1:-1]
        for elem in elemsToMod:
            licenseMan.applyLicenseToFiles(elem)
    else:
        print "Usage: ./license-applier.py <file/dir 1 ... file/dir n> license_file"

if __name__ == "__main__":
    main()




