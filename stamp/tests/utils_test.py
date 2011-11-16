import os
import unittest

from stamp import utils

class TestUtils(unittest.TestCase):
    """ """
    def setUp(self):
        self.nodotted_paths_list = ['test.c', 'test.py', 'blabla']
        self.dotted_paths_list = self.nodotted_paths_list + ['.taratata', '.blablabla', '.git']


    def test_get_file_extension(self):
        self.assertIsNone(utils.get_file_extension('test'))
        self.assertIsNone(utils.get_file_extension('/tmp/blabla'))

        self.assertIsNotNone(utils.get_file_extension('test.c'))
        self.assertIsNotNone(utils.get_file_extension('/tmp/blabla.py'))

        self.assertEqual(utils.get_file_extension('test.c'), 'c')
        self.assertEqual(utils.get_file_extension('/tmp/blabla.py'), 'py')
        self.assertEqual(utils.get_file_extension('test.C'), 'c')


    def test_remove_dotted_path_elements(self):
        """
        """
        self.assertIsNotNone(utils.remove_dotted_path_elements(self.nodotted_paths_list))
        self.assertIsNotNone(utils.remove_dotted_path_elements(self.dotted_paths_list))

        self.assertEqual(utils.remove_dotted_path_elements(self.nodotted_paths_list), self.nodotted_paths_list)
        self.assertEqual(utils.remove_dotted_path_elements(self.dotted_paths_list), self.nodotted_paths_list)

        # Asserting that given a string, the function returns
        # a list containing the given string if it was not dotted
#        self.assertIsInstance(utils.remove_dotted_path_elements('/tmp/test.c'), list)
#        self.assertIsInstance(utils.remove_dotted_path_elements('/tmp/.blabla'), list)
#        self.assertEqual(utils.remove_dotted_path_elements('/tmp/test.c'), ['test.c'])
#        self.assertEqual(utils.remove_dotted_path_elements('/tmp/.blabla'), '/tmp/.blabla)


    def tearDown(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
unittest.TextTestRunner(verbosity=2).run(suite)
