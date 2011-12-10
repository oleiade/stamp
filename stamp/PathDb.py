#!/usr/bin/env python

import os
import constants

class PathDb:
    """
    """
    def __init__(self):
        """Constructor"""
        self.user = os.environ["USER"]
        self.user_home = os.environ["HOME"]
        self.db = {}


    def load_from_file(self):
        """
        """
        pass


    def dump_to_file(self, file_path):
        """
        """
        pass


    def create(self, key, value):
        """
        """
        pass


    def read(self, key):
        """
        """
        pass


    def update(self, key, value):
        """
        """
        pass


    def delete(self, key):
        """
        """
        pass
