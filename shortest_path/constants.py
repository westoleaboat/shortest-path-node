from enum import Enum, auto
"""
A set of constants that will let us refer to the different 
field types in a consistent and explicit way
"""


class FieldTypes(Enum):
    # https://docs.python.org/3/library/enum.html
    """
    Store some named integer values.
    auto() function gives each constant of the class
    a unique integer value automatically.

    """

    string = auto()
    string_list = auto()
    short_string_list = auto()
    iso_date_string = auto()
    long_string = auto()
    decimal = auto()
    integer = auto()
    boolean = auto()
