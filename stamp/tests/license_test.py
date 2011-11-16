import os
import unittest

from stamp import License, constants

class TestLicense(unittest.TestCase):
    """

    """
    def setUp(self):
        test_license_file = os.path.join(os.path.dirname(__file__), 'valid_test_license_file.txt')
        self.inst = License.License(test_license_file)


    def test_is_valid_file_extension(self):
        self.assertFalse(self.inst.is_valid_file_extension('blablabla'))
        self.assertFalse(self.inst.is_valid_file_extension(''))

        self.assertTrue(self.inst.is_valid_file_extension(constants.LANG_EXTENSIONS.keys()[0]))
        self.assertTrue(self.inst.is_valid_file_extension('c'))
        self.assertTrue(self.inst.is_valid_file_extension('C'))


    def test_get_lang_from_extension(self):
        self.assertRaises(IndexError, self.inst.get_lang_from_extension, ('papadoudou'))
        self.assertRaises(IndexError, self.inst.get_lang_from_extension, (' '))

        self.assertIsNotNone(self.inst.get_lang_from_extension('c'))
        self.assertEqual(self.inst.get_lang_from_extension('c'), 'c')

        self.assertIsNotNone(self.inst.get_lang_from_extension('py'))
        self.assertEqual(self.inst.get_lang_from_extension('py'), 'python')

        self.assertIsNotNone(self.inst.get_lang_from_extension('PY'))
        self.assertEqual(self.inst.get_lang_from_extension('PY'), 'python')


    def test_as_dict(self):
        self.assertIsNotNone(self.inst.as_dict())
        self.assertIsInstance(self.inst.as_dict(), dict)
        self.assertIn('content', self.inst.as_dict())
        self.assertIn('size', self.inst.as_dict())


    def test_format_as(self):
        self.assertRaises(KeyError, self.inst.format_as, ('papdoudou'))

        self.assertIsNotNone(self.inst.format_as('C'))
        self.assertIsNotNone(self.inst.format_as('c'))

        self.assertIsInstance(self.inst.format_as('C'), list)
        self.assertEqual(self.inst.format_as('C')[0], constants.LANG_COMMENT_STYLE["stars"][0] + '\n')
        self.assertEqual(self.inst.format_as('C')[-1], constants.LANG_COMMENT_STYLE["stars"][-1] + '\n')


    def test_get_license_as(self):
        self.inst.get_license_as('C')

        self.assertIsNotNone(self.inst.buffered_licenses)
        self.assertIn('c', self.inst.buffered_licenses)  # buffer stores lowercase keys
        self.assertEqual(self.inst.buffered_licenses['c'],
                         self.inst.format_as('c'))

        self.assertNotIn('papadou', self.inst.buffered_licenses)
        self.assertNotIn('python', self.inst.buffered_licenses)


suite = unittest.TestLoader().loadTestsFromTestCase(TestLicense)
unittest.TextTestRunner(verbosity=2).run(suite)
