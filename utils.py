#!/usr/bin/env python

import os

def get_file_extension(path):
    """
    Extracts extension from file path.
    """
    _, file_extension = os.path.splitext(path)

    # return file_extension without it's
    # starting point
    return file_extension[1:]


def remove_dotted_path(path):
    """
    Removes dirs and files begginingg with dots
    from a given list, which could, for example,
    have been yielded by os.walk for example.

    path_list         List : path list where
    to search and remove those who begins with a dot.
    """
    # Keeping a flag value when given path is a string,
    str_flag = True if isinstance(path, str) else False

    # Encapsulating string in a list in order to keep dry
    # when path is a string. Selecting explicitly last part
    # of the path in order to avoir current working dir shortcut (./foo_bar)
    if str_flag:
        path_dump = path  # keeping a copy in order to return full path
        path = [path.split('/')[-1]]

    for (counter, elem) in enumerate(path):
        if elem.startswith('.'):
            del path[counter - 1]

    return path_dump if (str_flag and path) else path
