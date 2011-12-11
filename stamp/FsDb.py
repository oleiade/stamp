#!/usr/bin/env python

import os
import simplejson as json

from datetime import datetime

from constants import STAMP_DB_FILENAME


META_KEYS = "meta"
CONTAINERS_KEYS = "containers"

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
        try:
            db_key = self.__get_or_create_key(key)
        except KeyError:
            pass
        except ValueError:
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
            META_KEYS : {
                'owner': self.user,
                'storage_file_path': self.storage_file_path,
                'created_at': datetime.now().strftime("%d/%m/%Y"),
                'last_updated_at': datetime.now().strftime("%d/%m/%Y"),
            },
            CONTAINERS_KEYS : {
                'licenses': {},
                'paths': {},
            },
        }
        self.dump()

        return


    def update_meta(self, meta=None):
        """
        Updates the filesystem database meta datas with
        brand new dict taken from params, or updates
        it using the environement.
        """
        if meta:
            self.db[META_KEYS] = meta
        else:
            self.db[META_KEYS]["owner"] = self.user
            self.db[META_KEYS]["storage_file_path"] = self.storage_file_path
            self.db[META_KEYS]["last_updated_at"] = datetime.now().strftime("%d/%m/%Y")

        return



    def __get_or_create_key(self, key):
        """
        Get or creates a key in one of the containers dict
        of the database and returns it as a mutable object.

        Nota : the META informations were intended to be immutable.

        Keys should always be prefixed with a table name and
        can not be written at the root of the database tables root.
        Keys should be created using a redis-like pattern table:key.

        for example to create a key in order to store a path
        datas, you should use the methode like :
                self.__create_key("paths:path_to_the_file")
        """
        try:
            computed_table, computed_key = key.split(':')
        except ValueError:
            print "Invalid pattern used for key creation. \
            valid should look like table:key"
            sys.exit()

        db_table = self.db[CONTAINERS_KEYS].setdefault(computed_table, {})
        db_key = self.db[CONTAINERS_KEYS][computed_table].setdefault(computed_key, {})

        return db_key
