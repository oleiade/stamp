#!/usr/bin/env python

import unittest

def assertTuplesList(self, tuples_list):
    if tuples_list and len(tuples_list) > 0:
        for t in tuples_list:
            unittest.assertIsInstance(t, tuple)

def assertListsList(self, lists_list):
    if lists_list and len(lists_list) > 0:
        for t in lists_list:
            unittest.assertIsInstance(t, list)
