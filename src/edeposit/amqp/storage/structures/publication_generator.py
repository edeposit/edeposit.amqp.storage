#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from string import Template


# Variables ===================================================================
CLASS_NAME = "Publication"

COMMON_FIELDS = [
    ["title", "(str): Title of the publication."],
    ["author", "(str): Name of the author."],
    ["pub_year", "(str): Year when the publication was released."],
    ["isbn", "(str): ISBN for the publication."],
    ["urnnbn", "(str): URN:NBN for the publication."],
    ["uuid", "(str): UUID string to pair the publication with edeposit."],
    ["is_public", "(bool): Is the file public?"],
    ["format", "(str): Mime for the format."],
]

COMMUNICATION_FIELDS = [
    ["b64_data", "(str): Base64 encoded data ebook file."],
]

DATABASE_FIELDS = [
    ["file_pointer", "(str): Pointer to the file on the file server."],
]

TEMPLATE = """
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# Imports =====================================================================
$imports


# Functions and classes =======================================================

# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
$classes
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!

"""

COMMUNICATION_STRUCTURE = """
fields = [
    $fields
]

class $class_name(namedtuple('$class_name', fields)):
    '''
    Communication structure used to sent data to `storage` subsystem over AMQP.

    Attributes:
        $docstring_fields
    '''

"""


# Functions & classes =========================================================
def generate_communication():
    fields = "\n    ".join(
        name for name, x in COMMON_FIELDS + COMMUNICATION_FIELDS
    )

    docstring_fields = "\n        ".join(
        name + " " + description
        for name, description in COMMON_FIELDS + COMMUNICATION_FIELDS
    )

    return Template(COMMUNICATION_STRUCTURE).substitute(
        fields=fields,
        class_name=CLASS_NAME,
        docstring_fields=docstring_fields
    )


def generate_structures():
    pass


print generate_communication()