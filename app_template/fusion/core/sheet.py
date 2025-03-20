import typing
from fusion.core.column import Column
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import sqlalchemy.engine
import sqlalchemy.orm.session


class Sheet:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        # attribute columns is a list of Column objects
        self.columns: typing.List[Column] = []

    def __str__(self):
        return f"Sheet(name={self.name})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "columns": [column.to_dict() for column in self.columns],
        }

    def __repr__(self):
        return str(self)

    def add_column(self, column: Column):
        self.columns.append(column)

    def create_or_update_table(self, engine: sqlalchemy.engine.base.Connection):
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            self.id,
            metadata,
            *[
                sqlalchemy.Column(column.id, column.type.to_sqlalchemy_type())
                for column in self.columns
            ],
        )
        metadata.create_all(engine)
        return table
