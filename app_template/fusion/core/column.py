import typing

import sqlalchemy
from fusion.core.column_types import ColumnType


class Column:
    def __init__(self, id: str, name: str, type: ColumnType):
        self.id = id
        self.name = name
        self.type = type

    def __str__(self):
        return f"Column(name={self.name}, type={self.type})"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "type": self.type.name}

    def __repr__(self):
        return str(self)

    def to_sqlalchemy_type(self):
        if self.type == ColumnType.INT:
            return sqlalchemy.Integer
        elif self.type == ColumnType.STRING:
            return sqlalchemy.String
        elif self.type == ColumnType.FLOAT:
            return sqlalchemy.Float
        elif self.type == ColumnType.BOOL:
            return sqlalchemy.Boolean
        elif self.type == ColumnType.DATETIME:
            return sqlalchemy.DateTime
