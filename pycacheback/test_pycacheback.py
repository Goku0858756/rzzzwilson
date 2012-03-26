#!/usr/bin/env python

"""
Test pycacheback
"""

import os
import shutil
from pycacheback import pyCacheBack
import unittest


class TestpyCacheBack(unittest.TestCase):
    def testSimple(self):
        """A simple 'smoke test' for the extended dictionary."""

        # make an extended dictionary and define a key/value pair
        a = pyCacheBack()
        a[1] = 'one'

        # make sure we can retrieve the pre-defined key/value pair
        msg = "a[1] != 'one'!"
        self.assertEqual(a[1], 'one', msg)

        # make sure that accessing non-existant key raises KeyError
        self.assertRaises(KeyError, a.__getitem__, 2)

        # make sure the len() function works correctly
        msg = "len(a) should be 1, got %d!" % len(a)
        self.assertEqual(len(a), 1, msg)

    def testLRU(self):
        """Test the LRU mechanism."""

        # make an extended dictionary, maxLRU is 2 for testing
        a = pyCacheBack(2)

        # the LRU list should be empty when we start
        msg = ("Initial LRU list should be empty, but it's %s"
               % str(a._lru_list))
        self.assertEqual(a._lru_list, [], msg)

        # make sure the len() function works correctly
        msg = "len(a) should be 0, got %d!" % len(a)
        self.assertEqual(len(a), 0, msg)

        # add a key/value pair, recheck LRU
        a['test'] = 'test value'
        msg = ("LRU list should be %s, but it's %s"
               % (str(['test']), str(a._lru_list)))
        self.assertEqual(a._lru_list, ['test'], msg)

        # add another key/value pair, recheck LRU
        a['test2'] = 'another test value'
        msg = ("LRU list should be %s, but it's %s"
               % (str(['test2', 'test']), str(a._lru_list)))
        self.assertEqual(a._lru_list, ['test2', 'test'], msg)

        # access first key/value pair, check LRU changed
        b = a['test']
        msg = ("LRU list should be %s, but it's %s"
               % (str(['test', 'test2']), str(a._lru_list)))
        self.assertEqual(a._lru_list, ['test', 'test2'], msg)

        # make sure the len() function works correctly
        msg = "len(a) should be 2, got %d!" % len(a)
        self.assertEqual(len(a), 2, msg)

        # add third key/value pair, check LRU changed
        a['test3'] = 100
        msg = ("LRU list should be %s, but it's %s"
               % (str(['test3', 'test']), str(a._lru_list)))
        self.assertEqual(a._lru_list, ['test3', 'test'], msg)

        # make sure the len() function works correctly
        msg = "len(a) should be 2, got %d!" % len(a)
        self.assertEqual(len(a), 2, msg)

        # delete first key/value pair, check LRU changed
        del a['test']
        msg = ("LRU list should be %s, but it's %s"
               % (str(['test3']), str(a._lru_list)))
        self.assertEqual(a._lru_list, ['test3'], msg)

        # make sure the len() function works correctly
        msg = "len(a) should be 1, got %d!" % len(a)
        self.assertEqual(len(a), 1, msg)

    def testBacking(self):
        """Test the backing mechanism.  Keys will be (x, y) form."""

        # create the test directory
        test_dir = './test_dir'
        shutil.rmtree(test_dir, ignore_errors=True)
        os.mkdir(test_dir)

        # override the backing functions in pyCacheBack
        class my_cache(pyCacheBack):
            def _put_to_back(self, key, value):
                (x, y) = key
                dir_path = os.path.join(test_dir, str(x))
                try:
                    os.mkdir(dir_path)
                except OSError:
                    pass
                file_path = os.path.join(dir_path, str(y))
                with open(file_path, 'wb') as f:
                    f.write(str(value))

            def _get_from_back(self, key):
                raise KeyError
        # define utility testing function
        def check_file(self, file_path, expected_contents):
            if not os.path.isfile(file_path):
                self.fail("File %s doesn't exist!?" % file_path)
            with open(file_path, 'rb') as f:
                file_contents = f.read()
            if file_contents != expected_contents:
                self.fail("Expected file contents %s, got %s"
                          % (expected_contents, file_contents))

        # OK, test it
        a = my_cache(2)
        a[(1,1)] = 'one and one'
        a[(1,2)] = 'one and two'
        a[(1,1)] = 'one and one, second value'  # redefine (1,1) value

        # test if backing files are as expected
        check_file(self, os.path.join(test_dir, '1', '1'), a[(1,1)])
        check_file(self, os.path.join(test_dir, '1', '2'), a[(1,2)])

        # add third key, flushing (1,2), check backing file still there
        a[(1,3)] = 'one, three'
        check_file(self, os.path.join(test_dir, '1', '2'), a[(1,2)])

        # delete a key, check backing file still there
        del a[(1,3)]
        check_file(self, os.path.join(test_dir, '1', '3'),
                   'one, three')

        # clean up
        shutil.rmtree(test_dir)


unittest.main()