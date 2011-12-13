#!/usr/bin/env python

import os
import unittest
import simplejson as json

from datetime import datetime
from simplejson import JSONDecodeError

from stamp import FsDb
from stamp.FsDb import META_KEYS, CONTAINERS_KEYS
from stamp.constants import STAMP_DB_FILENAME

STAMP_DB_PATH = os.environ["HOME"] + '/' + STAMP_DB_FILENAME

class TestFsDb(unittest.TestCase):
    def __set_default_db(self):
        default_db = {
            META_KEYS : {
                'owner': os.environ["USER"],
                'storage_file_path': STAMP_DB_PATH,
                'created_at': datetime.now().strftime("%d/%m/%Y"),
                'last_updated_at': datetime.now().strftime("%d/%m/%Y"),
            },
            CONTAINERS_KEYS : {
                'licenses': {},
                'paths': {},
            },
        }

        return default_db

    def __set_default_db_file_dump(self):
        w_default_db_dump = open(self.default_db_file, 'w')
        r_default_db_dump = open(self.default_db_file, 'r+')

        json.dump(self.default_db, w_default_db_dump)
        w_default_db_dump.close()

        return r_default_db_dump


    def setUp(self):
        self.fsdb = FsDb.FsDb()
        self.default_db = self.__set_default_db()
        self.default_db_file = '/tmp/test_db_dump'
        self.default_db_file_dump = self.__set_default_db_file_dump()


    def test_init_in_memory_db_creation(self):
        self.fsdb.init()

        # Assert that in-memory db is correctly instantiated.
        self.assertIsInstance(self.fsdb.db, dict)
        self.assertIn(META_KEYS, self.fsdb.db)
        self.assertIn(CONTAINERS_KEYS, self.fsdb.db)


    def test_init_dump_to_file(self):
        self.fsdb.init()

        # assert that init dumps to the db file in user home.
        self.assertTrue(os.path.exists(STAMP_DB_PATH))

        # assert that the file dump is correctly instantiated
        # and has sane content.
        dump_fd = open(STAMP_DB_PATH, 'r+')
        loaded_db_dump = json.load(dump_fd)
        self.assertIsInstance(loaded_db_dump, dict)
        self.assertIn(META_KEYS, loaded_db_dump)
        self.assertIn(CONTAINERS_KEYS, loaded_db_dump)


    def test_update_meta_from_env(self):
        """Tests the basic meta is correctly initialized using env"""
        self.fsdb.init()
        self.fsdb.update_meta()

        self.assertIsInstance(self.fsdb.db[META_KEYS], dict)
        self.assertEqual(self.fsdb.db[META_KEYS]["owner"], os.environ["USER"])
        self.assertEqual(self.fsdb.db[META_KEYS]["storage_file_path"], STAMP_DB_PATH)


    def test_update_meta_from_dict(self):
        self.fsdb.init()
        meta_dump = self.fsdb.db[META_KEYS]
        new_meta = {
            'owner': 'test',
            'storage_file_path': 'test',
            'test_key': 'test',
        }

        self.fsdb.update_meta(new_meta)
        self.assertIn(META_KEYS, self.fsdb.db)
        self.assertIsInstance(self.fsdb.db[META_KEYS], dict)
        self.assertEqual(self.fsdb.db[META_KEYS], new_meta)


    def test_load_from_default(self):
        """Test load() method with default class attrs"""
        # Load the file content using simplejson, and force
        # FsDb instance to override it's content with it's load
        # method, in order to compare values.
        loaded_datas = json.load(self.default_db_file_dump)
        self.fsdb.load()

        self.assertIsNotNone(self.fsdb.db)
        self.assertIsInstance(self.fsdb.db, dict)
        self.assertEqual(loaded_datas, self.fsdb.db)


    def test_load_from_path(self):
        """Test load() method with a given file path in param"""
        # Load the file content using simplejson, and force
        # FsDb instance to override it's content with it's load
        # method using the same path as the one gived to simplejson
        # method, in order to compare values.
        loaded_datas = json.load(self.default_db_file_dump)
        self.fsdb.load(self.default_db_file)

        self.assertIsNotNone(self.fsdb.db)
        self.assertIsInstance(self.fsdb.db, dict)
        self.assertEqual(loaded_datas, self.fsdb.db)


    def test_load_fail_from_invalid_path(self):
        self.assertRaises(IOError, self.fsdb.load, ('/tmp'))


    def test_load_fail_from_invalid_file_format(self):
        fp = open('/tmp/test.c', 'w')
        fp.write('blablablabla, this is invalid')
        fp.close()
        with self.assertRaises(JSONDecodeError):
            self.fsdb.load(path='/tmp/test.c')


    def test_dump_to_default(self):
        pass


    def test_dump_to_path(self):
        pass


    def test_create_valid_key_value(self):
        pass


    def test_create_key_without_value(self):
        """Should pass"""
        pass


    def test_create_value_without_key(self):
        """Should fail"""
        pass


    def test_create_already_existing_key(self):
        """Should raise an already existing"""
        pass


    def test_create_invalid_key(self):
        """
        Keys should be alphanum characters string
        only
        """
        pass


    def test_read_existing_key(self):
        pass


    def test_read_not_existing_key(self):
        """Should raise a KeyError"""
        pass


    def test_read_existing_key(self):
        pass


    def test_update_not_existing_key(self):
        """Should raise exception"""
        pass


    def test_update_with_invalid_key(self):
        pass


    def test_update_incremental(self):
        """
        Should test that if the value stored
        at the given key, is a mutable struct type (dict,
        list, deques...), update is able to add values,
        without overriding the present values.
        """
        pass


    def test_delete_existing_key(self):
        pass


    def test_delete_not_existing_key(self):
        pass


    def test_vacuum(self):
        pass

    def tearDown(self):
        if os.path.exists(STAMP_DB_PATH):
            os.remove(STAMP_DB_PATH)

        self.default_db_file_dump.close()
        os.remove(self.default_db_file)


suite = unittest.TestLoader().loadTestsFromTestCase(TestFsDb)
unittest.TextTestRunner(verbosity=2).run(suite)
