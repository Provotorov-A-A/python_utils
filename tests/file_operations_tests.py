""" Tests of common utility procedures for file manipulation.

@author Provotorov A. merqcio11@gmail.com
"""


import sys
import os
import unittest
import inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
src_dir = os.path.join(currentdir, '..')
sys.path.insert(0, src_dir)


from file_operations import *


class TestParser(unittest.TestCase):
    test_data_dir = os.path.join(currentdir, 'data')
    tmp_dir_name = 'tmp'
    tmp_dir = os.path.join(test_data_dir, tmp_dir_name)
    nested_dir_name = 'nested'
    nested_dir = os.path.join(tmp_dir, nested_dir_name)

    def setUp(self):
        pass

    def tearDown(self) -> None:
        self.clean_tmp()

    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = file.read()
        except IOError:
            return None
        return data

    def write_file(self, filename, data):
        try:
            with open(filename, 'w') as file:
                file.write(data)
        except IOError:
            return False
        return True

    def test_create_dir(self):
        tmp_dir_exists = os.path.isdir(self.tmp_dir)
        if tmp_dir_exists:
            shutil.rmtree(self.tmp_dir)
        self.assertFalse(os.path.isdir(self.tmp_dir))

        # simple
        create_dir(self.tmp_dir_name, self.test_data_dir, recursively=False, overwrite=False)
        tmp_dir_exists = os.path.isdir(self.tmp_dir)
        self.assertTrue(tmp_dir_exists)
        os.rmdir(self.tmp_dir)
        self.assertFalse(os.path.isdir(self.tmp_dir))

        # recursively
        nested_dir_name = f'{self.tmp_dir_name}/nested'
        dir_ok = create_dir(nested_dir_name, self.test_data_dir, recursively=True, overwrite=False)
        self.assertTrue(dir_ok)
        nested_dir = os.path.join(self.test_data_dir, nested_dir_name)
        dir_exists = os.path.isdir(nested_dir)
        self.assertTrue(dir_exists)
        os.rmdir(nested_dir)
        self.assertFalse(os.path.isdir(nested_dir))
        os.rmdir(self.tmp_dir)
        self.assertFalse(os.path.isdir(self.tmp_dir))
        dir_ok = create_dir(nested_dir_name, self.test_data_dir, recursively=False, overwrite=False)
        self.assertFalse(dir_ok)
        self.assertFalse(os.path.isdir(nested_dir))

        # overwrite
        dir_ok = create_dir(nested_dir_name, self.test_data_dir, recursively=True, overwrite=False)
        self.assertTrue(dir_ok)
        filename = os.path.join(nested_dir, 'test.txt')
        Path(filename).touch(exist_ok=True)
        self.assertTrue(os.path.isfile(filename))
        dir_ok = create_dir(nested_dir_name, self.test_data_dir, recursively=True, overwrite=False)
        self.assertTrue(os.path.isfile(filename))
        dir_ok = create_dir(nested_dir_name, self.test_data_dir, recursively=True, overwrite=True)
        self.assertFalse(os.path.isfile(filename))
        # clean
        os.rmdir(nested_dir)
        self.assertFalse(os.path.isdir(nested_dir))
        os.rmdir(self.tmp_dir)
        self.assertFalse(os.path.isdir(self.tmp_dir))

    def init_tmp(self):
        create_dir(self.tmp_dir, overwrite=True, recursively=True)
        create_dir(self.nested_dir, overwrite=True, recursively=True)

    def test_remove_dir(self):
        #
        self.init_tmp()
        self.assertTrue(os.path.isdir(self.tmp_dir))

        #
        self.init_tmp()
        self.assertTrue(os.path.isdir(self.tmp_dir))
        nested_dir_name = f'{self.tmp_dir_name}/nested'
        dir_ok = create_dir(nested_dir_name, self.test_data_dir)
        self.assertTrue(dir_ok)
        nested_dir = os.path.join(self.test_data_dir, nested_dir_name)
        self.assertTrue(os.path.isdir(nested_dir))
        rem_dir = remove_dir(self.tmp_dir, recursively=False)
        self.assertFalse(rem_dir)
        self.assertTrue(os.path.isdir(nested_dir))
        rem_dir = remove_dir(self.tmp_dir, recursively=True)
        self.assertTrue(rem_dir)
        self.assertFalse(os.path.isdir(nested_dir))

    def clean_tmp(self):
        remove_dir(self.tmp_dir, recursively=True)

    def test_create_file(self):
        self.init_tmp()
        fname = 'test.txt'
        f = os.path.join(self.nested_dir, fname)
        self.assertFalse(os.path.isfile(f))
        ok = create_file(fname, self.nested_dir, overwrite=False)
        self.assertTrue(ok)
        self.assertTrue(os.path.isfile(f))
        valid_data = 'TEST'
        wr_ok = self.write_file(f, valid_data)
        self.assertTrue(wr_ok)
        # no ow
        ok = create_file(fname, self.nested_dir, overwrite=False)
        self.assertTrue(ok)
        self.assertTrue(os.path.isfile(f))
        rd = self.read_file(f)
        self.assertIsNotNone(rd)
        self.assertEqual(valid_data, rd)
        # ow
        ok = create_file(fname, self.nested_dir, overwrite=True)
        self.assertTrue(ok)
        self.assertTrue(os.path.isfile(f))
        rd = self.read_file(f)
        self.assertEqual('', rd)
        # complex name
        self.clean_tmp()
        fname = os.path.join(self.nested_dir_name, 'test.txt')
        f = os.path.join(self.tmp_dir, fname)
        self.assertFalse(os.path.isfile(f))
        ok = create_file(fname, self.tmp_dir, overwrite=False)
        self.assertTrue(ok)
        self.assertTrue(os.path.isfile(f))
        valid_data = 'TEST'
        wr_ok = self.write_file(f, valid_data)
        self.assertTrue(wr_ok)

        self.clean_tmp()

    def test_remove_file(self):
        self.init_tmp()

        #
        fname = 'test.txt'
        f = os.path.join(self.nested_dir, fname)
        self.assertFalse(os.path.isfile(f))
        ok = create_file(fname, self.nested_dir, overwrite=False)
        self.assertTrue(os.path.isfile(f))
        remove_file(fname, self.nested_dir)
        self.assertFalse(os.path.isfile(f))

        #
        fname = os.path.join(self.nested_dir_name, 'test.txt')
        f = os.path.join(self.tmp_dir, fname)
        self.assertFalse(os.path.isfile(f))
        ok = create_file(fname, self.tmp_dir, overwrite=False)
        self.assertTrue(os.path.isfile(f))
        remove_file(fname, self.tmp_dir)
        self.assertFalse(os.path.isfile(f))

        self.clean_tmp()

    def test_remove_files(self):
        self.init_tmp()

        files = ['apple.txt', 'test.txt', 'cfg.json']
        for f in files:
            create_file(f, self.nested_dir)
        self.assertEqual(len(files), len(os.listdir(self.nested_dir)))

        ok = remove_files(self.nested_dir)
        self.assertTrue(ok)
        self.assertEqual(0, len(os.listdir(self.nested_dir)))

        self.clean_tmp()

    def test_copytree(self):
        self.init_tmp()

        files: list = ['apple.txt', 'test.txt', 'cfg.json']
        for f in files:
            self.assertTrue(create_file(f, self.nested_dir))
        self.assertEqual(len(files), len(os.listdir(self.nested_dir)))
        dst_dir = os.path.join(self.tmp_dir, 'dst')
        dir_ok = create_dir(dst_dir)
        self.assertTrue(dir_ok)

        copytree(self.tmp_dir, dst_dir)
        self.assertEqual(2, len(os.listdir(dst_dir)))
        dst_nested_dir = os.path.join(dst_dir, self.nested_dir_name)
        self.assertTrue(os.path.isdir(dst_nested_dir))
        self.assertTrue(os.path.isdir(os.path.join(dst_dir, 'dst')))
        self.assertEqual(len(files), len(os.listdir(dst_nested_dir)))
        dst_files = os.listdir(dst_nested_dir)
        self.assertListEqual(sorted(files), sorted(dst_files))

        self.clean_tmp()

    def test_copy_file(self):
        self.init_tmp()

        org_fname = 'origin.txt'
        org_file = os.path.join(self.tmp_dir, org_fname)
        create_file(org_file)
        self.assertTrue(os.path.isfile(org_file))
        valid_data_1 = 'TEST_DATA_1'
        self.write_file(org_file, valid_data_1)

        dst_dir = self.nested_dir
        dst_fname = 'copy.txt'
        dst_file = os.path.join(dst_dir, dst_fname)

        # copy to file
        ok = copy_file(org_file, dst_file, overwrite=False)
        self.assertTrue(ok)
        self.assertTrue(os.path.isfile(dst_file))
        rd = self.read_file(dst_file)
        self.assertEqual(valid_data_1, rd)

        # copy to existing file, ov = False
        valid_data_2 = 'TEST_DATA_2'
        self.write_file(org_file, valid_data_2)
        ok = copy_file(org_file, dst_file, overwrite=False)
        self.assertTrue(ok)
        self.assertTrue(os.path.isfile(dst_file))
        rd = self.read_file(dst_file)
        self.assertEqual(valid_data_1, rd)

        # copy to existing file, ov = True
        ok = copy_file(org_file, dst_file, overwrite=True)
        self.assertTrue(ok)
        self.assertTrue(os.path.isfile(dst_file))
        rd = self.read_file(dst_file)
        self.assertEqual(valid_data_2, rd)

        self.clean_tmp()

    def test_find_file(self):
        self.init_tmp()

        fname = 'apple.txt'
        files: list = [fname, 'test.txt', 'cfg.json']
        for f in files:
            self.assertTrue(create_file(f, self.nested_dir))
        self.assertEqual(len(files), len(os.listdir(self.nested_dir)))

        # recursively = False
        result = find_file(fname, self.nested_dir, recursively=False)
        expected_result = os.path.join(self.nested_dir, fname)
        self.assertEqual(expected_result, result)

        result = find_file(fname, self.tmp_dir, recursively=False)
        expected_result = ''
        self.assertEqual(expected_result, result)

        # recursively = True
        result = find_file(fname, self.nested_dir, recursively=True)
        expected_result = os.path.join(self.nested_dir, fname)
        self.assertEqual(expected_result, result)

        result = find_file(fname, self.tmp_dir, recursively=True)
        self.assertEqual(expected_result, result)

        fname = 'invalid_name'
        result = find_file(fname, self.tmp_dir, recursively=True)
        expected_result = ''
        self.assertEqual(expected_result, result)

        # dir
        fname = 'apple.txt'
        result = find_file(fname, self.test_data_dir, recursively=True, is_dir=True)
        expected_result = ''
        self.assertEqual(expected_result, result)

        fname = self.nested_dir_name
        result = find_file(fname, self.test_data_dir, recursively=False, is_dir=True)
        expected_result = ''
        self.assertEqual(expected_result, result)

        result = find_file(fname, self.test_data_dir, recursively=True, is_dir=True)
        expected_result = self.nested_dir
        self.assertEqual(expected_result, result)

        self.clean_tmp()
