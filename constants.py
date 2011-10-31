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


LANG_COMMENT_FAMILY = {
            "stars": ["c", "c++", "js", "php"],
            "sharps": ["python", "perl"],
            "semicolon": ["elisp"]
            }


# Tuple should always have three elems,
# a prefix, content comment, suffix.
LANG_COMMENT_STYLE = {
    "stars": ('/*', '**', '*/'),
    "sharps": ('', '#', ''),
    "semicolon": ('', ';;', ''),
    }
