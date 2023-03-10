""" Common utility procedures for file manipulation.

Most of the procedures returns True in case of success and False in other case. Exceptions are ignored.

@author Provotorov A. merqcio11@gmail.com
"""


import os
import shutil
from pathlib import Path
from string_operations import strcmp


def find_file(name: str, path: str = '', ignore_case: bool = False, is_dir: bool = False, recursively: bool = True):
    """Returns full path of first occurrence of file or folder in specified directory (or nested directories).
    """
    _NO_RESULT = ''

    if not os.path.isdir(path):
        return _NO_RESULT

    type_cond = lambda fs_obj, isdir: (isdir and os.path.isdir(fs_obj)) or (not isdir and os.path.isfile(fs_obj))

    if not recursively:
        full_name = os.path.join(path, name)
        obj_list = os.listdir(path)
        for obj in obj_list:
            obj_fullname = os.path.join(path, obj)
            if type_cond(obj_fullname, is_dir) and strcmp(full_name, obj_fullname, ignore_case):
                return obj_fullname
        return _NO_RESULT
    else:
        for root, dirs, files in os.walk(path):
            if is_dir:
                if name in dirs:
                    return os.path.join(root, name)
            else:
                if name in files:
                    return os.path.join(root, name)
    return _NO_RESULT


def remove_file(name: str, path: str = ''):
    """Tries to remove file(folder) in specified folder. Returns True if object was successfully removed.
    """
    full_name = os.path.join(path, name)
    if os.path.isfile(full_name):
        try:
            os.remove(full_name)
        except OSError:
            return False
    return not os.path.isfile(full_name)


def remove_files(path: str):
    """Remove all files in specified folder. Returns True if files were successfully removed. Stops on first error.
    """
    if os.path.isdir(path):
        for obj_name in os.listdir(path):
            if not remove_file(obj_name, path):
                return False
    return True


def remove_dir(name: str, path: str = '', recursively: bool = False):
    """Tries to remove directory in specified folder. Returns True if it was successfully removed.
    """
    dir_name = os.path.dirname(name)
    full_dir = os.path.join(path, dir_name)
    if os.path.isdir(full_dir):
        full_name = os.path.join(path, name)
        try:
            if recursively:
                shutil.rmtree(full_name)
            else:
                os.rmdir(full_name)
        except OSError:
            return False
    return True


def create_dir(name: str, path: str = '', recursively: bool = True, overwrite: bool = False):
    """ Creates directory. Returns True if directory is created or already exists.
    """
    fullname: str = os.path.join(path, name)
    exists = os.path.exists(fullname)
    isdir = os.path.isdir(fullname)
    if exists:
        if overwrite:
            if isdir:
                try:
                    shutil.rmtree(fullname)
                except Exception as e:
                    return False
            else:
                return False
        else:
            return isdir
    try:
        Path(fullname).mkdir(parents=recursively, exist_ok=False)
    except Exception:
        return False
    return True


def create_file(name: str, path: str = '', overwrite: bool = False):
    """ Creates file and all parent directories. Returns True only if new file is successfully created.
    """
    fullname: str = os.path.join(path, name)
    parent_dir = os.path.dirname(fullname)
    exists = os.path.exists(fullname)
    if exists:
        if overwrite:
            if not remove_file(fullname):
                return False
        else:
            return False
    if not create_dir(parent_dir, recursively=True, overwrite=False):
        return False
    try:
        Path(fullname).touch(exist_ok=True)
    except Exception:
        return False
    return True


def copy_file(src_name: str, dst, src_path: str = '', overwrite: bool = False):
    """Copy src file to dst file or folder. Returns True if file is actually copied.
    """
    fullname: str = os.path.join(src_path, src_name)
    if not os.path.isfile(fullname):
        return False

    if os.path.isfile(dst):
        if overwrite:
            if not remove_file(dst):
                return False
        else:
            return False

    try:
        shutil.copy(fullname, dst)
    except OSError:
        return False
    return True


def copytree(src, dst, symlinks=False):
    """Copy all files and directories from src to dst.
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        try:
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, None)
            else:
                shutil.copy2(s, d)
        except OSError:
            return False
    return True

