#!/usr/bin/env python

import os
import simplejson as json

from datetime import datetime


from constants import STAMP_DB_FILENAME

class FsDb(object):
    """
    """
    def __init__(self):
        """Constructor"""
        self.user = os.environ["USER"]
        self.user_home = os.environ["HOME"]
        self.storage_file_path = self.user_home + '/' + STAMP_DB_FILENAME
        self.db = {}  # Fs database memory dump


    def load(self, path=None):
        """

        path            String : path to the file to load
                        database from.
        """
        fp = open(self.storage_file_path, 'r+')

        try:
            self.db = json.load(fp)
            fp.close()
        except IOError as (strerror, errno):
            print "I/O error({0}): {1}".format(errno, strerror)

        return


    def dump(self, file_path=None):
        """

        obj             String / File : Input to dump database from.
                        file path (string) or a yet openend file descriptor.
        """
        f = file_path if file_path else self.storage_file_path
        fp = open(f, 'w')

        try:
            json.dump(self.db, fp, indent=4)
            fp.close()
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


    def vaccum(self):
        """
        """
        pass


    def init(self):
        """
        Initialize the database structure with a minimal
        skeleton. Creates the storage file, and dumps
        minimal values to it, if not yet present.
        """
        self.db = {
            'owner': self.user,
            'storage_file_path': self.storage_file_path,
            'created_at': datetime.now().strftime("%d/%m/%Y"),
            'last_updated_at': datetime.now().strftime("%d/%m/%Y"),
        }
        self.dump()

        return

