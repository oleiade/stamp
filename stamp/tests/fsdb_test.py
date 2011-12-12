#!/usr/bin/env python

import os
import unittest
import simplejson as json

from stamp import FsDb
from stamp.FsDb import META_KEYS, CONTAINERS_KEYS
from stamp.constants import STAMP_DB_FILENAME

STAMP_DB_PATH = os.environ["HOME"] + '/' + STAMP_DB_FILENAME

class TestFsDb(unittest.TestCase):
    def setUp(self):
        self.fsdb = FsDb.FsDb()


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


    def tearDown(self):
        if os.path.exists(STAMP_DB_PATH):
            os.remove(STAMP_DB_PATH)


suite = unittest.TestLoader().loadTestsFromTestCase(TestFsDb)
unittest.TextTestRunner(verbosity=2).run(suite)
