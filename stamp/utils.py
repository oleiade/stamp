#!/usr/bin/env python

import os

def get_file_extension(path):
    """
    Extracts extension from file path.
    """
    _, extension = os.path.splitext(path)

    # return file_extension without it's
    # starting point
    file_extension = extension[1:].lower() if extension[1:] != '' else None

    return file_extension


def remove_dotted_path_elements(path):
    """
    Removes dirs and files begginingg with dots
    from a given path element list or string,
    which could, for example, have been yielded by os.walk.

    path_elem         List/String : path element where
    to search and remove those who begins with a dot.
    """
    # Encapsulating string in a list in order to keep dry
    # when path is a string. Selecting explicitly last part
    # of the path in order to avoir current working dir shortcut (./foo_bar)
    for (counter, elem) in enumerate(path):
        if elem.startswith('.'):
            del path[counter]

    return path
