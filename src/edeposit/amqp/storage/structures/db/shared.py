#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import base64
import zipfile
import os.path
import tempfile


# Functions & classes =========================================================
def path_to_zip(path):
    """
    Compress `path` to the ZIP.

    Args:
        path (str): Path to the directory.

    Returns:
        str: Path to the zipped file (in /tmp).
    """
    if not os.path.exists(path):
        raise IOError("%s doesn't exists!" % path)

    with tempfile.NamedTemporaryFile(delete=False) as ntf:
        zip_fn = ntf.name

    with zipfile.ZipFile(zip_fn, mode="w") as zip_file:
        for root, dirs, files in os.walk(path):
            for fn in files:
                zip_file.write(os.path.join(root, fn))

    return zip_fn


def read_as_base64(fn):
    """
    Convert given `fn` to base64 and return it. This method does the process
    in not-so-much memory consuming way.

    Args:
        fn (str): Path to the file which should be converted.

    Returns:
        str: File encoded as base64.
    """
    with open(fn) as unpacked_file:
        with tempfile.TemporaryFile() as b64_file:
            base64.encode(unpacked_file, b64_file)
            b64_file.flush()

            b64_file.seek(0)
            return b64_file.read()
