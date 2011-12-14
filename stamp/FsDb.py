#!/usr/bin/env python

import os
import simplejson as json

from datetime import datetime

from constants import STAMP_DB_FILENAME


META_KEYS = "meta"
CONTAINERS_KEYS = "containers"

class FsDb(object):
    """
    A CRUD mini key/value database system, dedicated to store
    datas about a filesystem structure. For example, used by the
    Stamper class, it will store every needed informations about
    walked through paths and patched files, licenses used to patched
    it and so on...

    Stores itself in user home directory as STAMP_DB_FILENAME, using
    JSON format. It's automatic behavior is to try to load itself from
    that place when instantiated (though a specific place can even be given
    to load method). If no db is found at the specified place, a basic one
    will be created with few META keys and basic CONTAINERS.

    Every operations are computed in ram memory, and dumped into the database
    file on __del__, or on explicit call to dump method.

    Keys syntax is following a redis-like pattern : container:key, it is important
    that the container name prefixes the key. Though container: will create a new
    container, creating a single :key is not possible.
    """
    def __init__(self, db_path=None):
        """
        Constructor

        db_path         String : path to load database content from
                        at instantiation.
        """
        self.user = os.environ["USER"]
        self.user_home = os.environ["HOME"]
        self.storage_file_path = db_path if db_path else self.user_home + '/' + STAMP_DB_FILENAME

        if os.path.exists(self.storage_file_path):
            # if db_path has been given, then use it to load
            # the db dump, else it will naturally use the
            # storage_file_path
            self.load(db_path)
        else:
            self.db = {}  # Fs database memory dump
            self.init()


    def __del__(self):
        """
        Destructor. Basically dumps the database operations
        to the database file before garbage collection operations.

        db_path         String : path to load database content from
                        at instantiation.
        """
        self.dump()

    def load(self, path=None):
        """
        Loads a database dump from JSON file. If path param
        is None, will compute the path where it's stored from
        the environement, following the $HOME/STAMP_DB_FILENAME
        pattern.

        path            String : path to the file to load
                        database from.
        """
        path = path if path else self.storage_file_path

        fp = open(path, 'r')
        self.db = json.load(fp)
        fp.close()

        return


    def dump(self, path=None):
        """
        Dumps a database dump file to the in-memory FsDb db
        class attribute. If path param is None, will compute
        the path where it's stored from the environement,
        following the $HOME/STAMP_DB_FILENAME pattern.

        path            String : Input to dump database from.
                        file path (string) or a yet openend file descriptor.
        """
        f = path if path else self.storage_file_path

        try:
            fp = open(f, 'w')
            json.dump(self.db, fp, indent=4)
            fp.close()
        except IOError as (strerror, errno):
            print "I/O error({0}): {1}".format(errno, strerror)

        return


    def create(self, key, value=None):
        """
        Creates a key/value pair in the database. A container
        has to be specified, using the redis-like FsDb syntax:
        container:key.
        Cf : __get_or_create docstring.

        key             String : key to create or get, following the
                        redis-like pattern (container:key)
        value           _ : any value type to store at database container key
        """
        db_key = self.__get_or_create_key(key)

        # update value, only if retrieved or create key
        # has no content/value yet.
        if not db_key:
            self.__set_key(key, value)

        return


    def read(self, key):
        """
        Retrieves a value from a database container key.

        key             String : key to retrieve value from, following the
                        redis-like pattern (container:key)
        """
        value = self.__get_key(key)

        return value if value != -1 else None


    def update(self, key, value):
        """
        Updates an existing key value with the one given
        as param. If key does not already exist, will result
        in a KeyError.

        key             String : key which value has to be updated,
                        following the redis-like pattern (container:key)
        value           _ : any value type to store at database container key
        """
        self.__set_key(key, value)

        return

    def delete(self, key):
        """
        Removes the value stored at the given key
        param from the database.
        key             String : key to delete, following the
                        redis-like pattern (container:key)
        """
        self.__del_key(key)

        return True

    def vaccum(self):
        """
        FIXME tag0.0.3
        """
        pass


    def init(self):
        """
        Initialize the database structure in-memory with
        a minimal skeleton. Creates the storage file, and dumps
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

        meta            Dict : meta datas to set into database.
                        overrides stored datas.
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

        key             String : key to create or get, following the
                        redis-like pattern (container:key)
        """
        if key.replace(":", "", 1).isalnum():
            try:
                computed_container, computed_key = key.split(':')
            except ValueError:
                # if there are no semicolon in key string, then
                # we can consider that only a container was given.
                computed_container = key
        else:
            raise ValueError("Keys should be made of two alnum strings with ':' separator")

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

        key             String : key to create or get, following the
                        redis-like pattern (container:key)
        """
        computed_container, computed_key = self.__compute_key(key)

        if computed_container and computed_key:
            db_table = self.db[CONTAINERS_KEYS].setdefault(computed_container, {})
            db_key = self.db[CONTAINERS_KEYS][computed_container].setdefault(computed_key, {})
        else:
            raise KeyError("Whether container or key is missing")



        return db_key


    def __get_key(self, key):
        """
        Retrieves a database key/value pair.
        Returns -1 and shows the KeyError exception
        when requested key doesn't exist.

        key             String : key which value should be retrieved from,
                        following the redis-like pattern (container:key)

        """
        computed_container, computed_key = self.__compute_key(key)
        value = None

        if computed_container and computed_key:
            value = self.db[CONTAINERS_KEYS][computed_container][computed_key]
        elif computed_container and not computed_key:
            value = self.db[CONTAINERS_KEYS][computed_container]
        else:
            raise KeyError("Requested key doesn't exist")

        return value

    def __set_key(self, key, value=None):
        """
        Updates a database key with value. Fails if
        pointed key doesn't already exist.

        key             String : key which value has to be updated,
                        following the redis-like pattern (container:key)
        value           _ : any value type to store at database container key
        """
        computed_container, computed_key = self.__compute_key(key)

        if computed_container and computed_key:
            self.db[CONTAINERS_KEYS][computed_container][computed_key] = value
        elif computed_container and not computed_key:
            self.db[CONTAINERS_KEYS][computed_container] = value
        else:
            raise KeyError("Whether the given container or key does not exist")

        return


    def __del_key(self, key):
        """
        Removes a database container key. Fails
        if key doesn't already exist.

        key             String : key to delete, following the
                        redis-like pattern (container:key)
        """
        computed_container, computed_key = self.__compute_key(key)

        if computed_container and computed_key:
            del(self.db[CONTAINERS_KEYS][computed_container][computed_key])
        elif computed_container:
            del(self.db[CONTAINERS_KEYS][computed_container])
        else:
            raise KeyError("Whether the computed key or container doesn't exist in database")

        return