#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import templates


# Main program ================================================================
if __name__ == '__main__':
    with open("publication.py", "wt") as f:
        f.write(templates.get_publication())

    with open("db_publication.py", "wt") as f:
        f.write(templates.get_db_publication())

    with open("archive.py", "wt") as f:
        f.write(templates.get_archive())

    with open("db_archive.py", "wt") as f:
        f.write(templates.get_db_archive())