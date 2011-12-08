#!/usr/bin/env python
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import os

def get_file_extension(file_path):
    """
    Extracts extension from file path.

    file_path           String : path to fetch extension from
    """
    _, extension = os.path.splitext(file_path)

    # return file_extension without it's
    # starting point
    file_extension = extension[1:].lower() if extension[1:] != '' else None

    return file_extension


def remove_dotted_path_elements(path):
    """
    Removes dirs and files begginingg with dots
    from a given path element list or string,
    which could, for example, have been yielded by os.walk.

    path                List/String : path element where
                        to search and remove those which
                        begins with a dot.
    """
    if isinstance(path, str):
        path = [path]

    # Encapsulating string in a list in order to keep dry
    # when path is a string. Selecting explicitly last part
    # of the path in order to avoir current working dir shortcut (./foo_bar)
    for (counter, elem) in enumerate(path):
        if elem.startswith('.'):
            del path[counter]

    return path[0] if len(path) == 1 else path


def chunker(iterable, chunksize):
    """
    Generates an iterator which returns chunks
    of the given iterable.

    Nota Bene : won't fill the last chunk with
    None or whatever in case chunksize is not a
    multiple of the iterable size.

    iterable            Iterable : iterable structure to cut into
                        sub-parts.
    chunksize           Int : size of sub-parts the iterable should
                        be cut into.
    """
    return (iterable[pos:pos + chunksize] for pos in xrange(0, len(iterable), chunksize))


def slice_tuples_list(tuples_list, index):
    """
    Returns a list of element sliced from tuples in a list.
    example : slice_tuples_list([(1,2,3), (4,5,6)], 0) => [1,4]
              slice_tuples_list([('abc', 'def'), ('ghi', 'jkl')], 1) => ['def', 'jkl'])
    """
    return [x[index] for x in tuples_list]

