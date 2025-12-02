from typing import Type
from app.db.database_connection import Database
from app.models.model_template import Model
from typing import TypeVar, Type

T = TypeVar("T", bound=Model)


class Relational(Model):

    @classmethod
    def listMatching(cls, column: str, id: int, match: Type[T]) -> list[T]:
        rows = Database.select(_from=cls.TABLE_NAME, where=f"{column} = {id}")
        return [match.instanceFromDatabaseRow(row) for row in rows]
