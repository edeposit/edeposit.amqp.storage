#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================



# Variables ===================================================================



# Functions & classes =========================================================
class Publication(object):
    def __init__(self):
        title = "(str): Title of the publication."
        author = "(str): Name of the author."
        pub_year = "(str): Year when the publication was released."
        isbn = "(str): ISBN for the publication."
        urnnbn = "(str): URN:NBN for the publication."
        uuid = "(str): UUID string to pair the publication with edeposit."
        is_public = "(bool): Is the file public?"
        format = "(str): Mime for the format."

        b64_data = "(str): Base64 encoded data ebook file."
        file_pointer = "(str): Pointer to the file on the file server."


# Použít nějaký generátor, aby byla stejná komunikační struktura i struktura
# v "databázi"?