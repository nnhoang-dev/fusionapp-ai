# Enum for column types
from enum import Enum


class ColumnType(Enum):
    STRING = 1
    INT = 2
    FLOAT = 3
    BOOL = 4
    DATETIME = 5
    DATE = 6
    TIME = 7
    FILE = 8
    IMAGE = 9
    VIDEO = 10
    AUDIO = 11
    URL = 12
    EMAIL = 13
    PHONE = 14
    OBJECT = 15
