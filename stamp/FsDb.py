#!/usr/bin/env python

import os
import simplejson as json

from datetime import datetime


from constants import STAMP_DB_FILENAME

class FsDb:
    """
    """
    def __init__(self):
        """Constructor"""
        self.user = os.environ["USER"]
        self.user_home = os.environ["HOME"]
        self.storage_path = self.user_home + STAMP_DB_FILENAME
        self.storage_file = open(self.storage_path, 'r+')
        self.db = {}  # Fs database memory dump


    def __del__(self):
        """Destructor"""
        self.storage_file.close()


    def load(self, path=None):
        """

        path            String : path to the file to load
                        database from.
        """
        try:
            self.db = json.load(self.storage_file)
        except IOError as (strerror, errno):
            print "I/O error({0}): {1}".format(errno, strerror)

        return


    def dump(self, file_path=None):
        """

        obj             String / File : Input to dump database from.
                        file path (string) or a yet openend file descriptor.
        """
        f = self.storage_file

        if file_path:
            f = open(file_path, 'r+')

        try:
            json.dump(self.db, f)
        except IOError as (strerror, errno):
            print "I/O error({0}): {1}".format(errno, strerror)

        return


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


    def init_db(self):
        """
        Initialize the database structure with a minimal
        skeleton. Creates the storage file, and dumps
        minimal values to it, if not yet present.
        """
        self.db = {
            'owner': self.user,
            'storage_path': self.storage_path,
            'created_at': datetime.now(),
            'last_updated_at': datetime.now(),
        }
        self.dump()

        return
