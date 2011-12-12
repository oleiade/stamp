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
            self.__get_or_create_key(key)
            self.__set_key(key, value)
        except KeyError:
            print "Invalid key name or pattern when trying to create a key/value pair."

        return

    def read(self, key):
        """
        """
        try:
            value = self.__get_or_create_key(key)
        except KeyError:
            print "The key does not exist in databases containers"

        return value


    def update(self, key, value):
        """
        """
        self.__set_key(key, value)


    def delete(self, key):
        """
        """
        self.__del_key(key)

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


    def __compute_key(self, key):
        """
        Returns a container/key pair computed
        from a given string. Enables to query the
        database using a redis-like syntax.

        a key should canonically look like:
                "container:key"
                for ex:
                "paths:/tmp/thisisafirsttestpath"
        """
        try:
            computed_container, computed_key = key.split(':')
        except ValueError:
            print "Invalid pattern used for key creation. \
            valid should look like table:key"

        return computed_container, computed_key


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
        computed_container, computed_key = self.__compute_key(key)

        db_table = self.db[CONTAINERS_KEYS].setdefault(computed_container, {})
        db_key = self.db[CONTAINERS_KEYS][computed_container].setdefault(computed_key, {})

        return db_key


    def __set_key(self, key, value):
        """
        Updates a database key with value.
        """
        computed_container, computed_key = self.__compute_key(key)

        try:
            if computed_container and computed_key:
                self.db[CONTAINERS_KEYS][computed_container][computed_key] = value
            elif computed_container:
                self.db[CONTAINERS_KEYS][computed_container] = value
        except KeyError:
            print "Whether the given container or key does not exist"

        return


    def __del_key(self, key):
        """
        Removes a database key.
        """
        computed_container, computed_key = self.__compute_key(key)

        try:
            if computed_container and computed_key:
                del(self.db[CONTAINERS_KEYS][computed_container][computed_key])
            elif computed_container:
                del(self.db[CONTAINERS_KEYS][computed_container]
        except KeyError:
            print "Whether the computed key or container doesn't exist in database"

        return