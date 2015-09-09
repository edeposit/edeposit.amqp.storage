#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import shutil
import os.path
import tempfile
import subprocess

import sh  # TODO: remove

from string import Template
from multiprocessing import Process

from storage import zconf
from storage import settings


# Variables ===================================================================
SERV = None
TMP_DIR = None


# Functions & classes =========================================================
def data_context(fn, mode="r"):
    path = os.path.join(os.path.dirname(__file__), "data")

    with open(os.path.join(path, fn), mode) as f:
        return f.read()


def generate_environment():
    global TMP_DIR
    TMP_DIR = tempfile.mkdtemp()

    # monkey patch the paths
    settings.ZCONF_PATH = TMP_DIR
    zconf.ZCONF_PATH = TMP_DIR

    # write ZEO server config to  temp directory
    zeo_conf_path = os.path.join(TMP_DIR, "zeo.conf")
    with open(zeo_conf_path, "w") as f:
        f.write(
            Template(data_context("zeo.conf")).substitute(path=TMP_DIR)
        )

    # write client config to temp directory
    client_config_path = os.path.join(TMP_DIR, "zeo_client.conf")
    with open(client_config_path, "w") as f:
        f.write(data_context("zeo_client.conf"))

    # run the ZEO server
    def run_zeo():
        # subprocess.check_call("runzeo -C " + zeo_conf_path, shell=True)
        sh.runzeo(C=zeo_conf_path)

    global SERV
    SERV = Process(target=run_zeo)
    SERV.start()


def cleanup_environment():
    SERV.terminate()
    shutil.rmtree(TMP_DIR)
