from datetime import date
from app.models.model_template import Model
from app.models.model_card import Card
from app.db.database_connection import Database


class Column(Model):

    MAX_NAME_LENGTH = 255
    TABLE_NAME = "tb_column"

    def __init__(self,
                 name: str,
                 position: int,
                 public_work_id: int) -> None:

        self.setName(name)
        self.setPosition(position)
        self.__setPublicWorkId(public_work_id)

    def __setPublicWorkId(self, public_work_id: int):
        if not isinstance(public_work_id, int):
            raise ValueError("Column public_work_id must be an integer.")
        if public_work_id <= 0:
            raise ValueError("Column public_work_id must be greater than 0.")
        self.__public_work_id = public_work_id

    def setName(self, name: str):

        if not isinstance(name, str):
            raise ValueError("Column name must be a string.")

        if len(name) > self.MAX_NAME_LENGTH:
            error = f"Column name length must be under {self.MAX_NAME_LENGTH}."
            raise ValueError(error)

        self.__name = name

    def setPosition(self, position: int):

        if not isinstance(position, int):
            raise ValueError("Column position must be an integer.")

        if position <= 0:
            raise ValueError("Column position must be greater than 0.")

        self.__position = position

    def getData(self) -> dict:
        return {
            "name": self.getName(),
            "position": self.getPosition(),
            "public_work_id": self.getPublicWorkId()
        }

    def getName(self) -> str:
        return self.__name

    def getPosition(self) -> int:
        return self.__position

    def getPublicWorkId(self) -> int:
        return self.__public_work_id

    def listCards(self) -> list[Card]:
        tb_card = Card.TABLE_NAME
        column_match = f"column_id = {self.getId()}"
        rows = Database.select(_from=tb_card, where=column_match)
        return [Card.instanceFromDatabaseRow(row) for row in rows]

    def getCard(self, position: int) -> Card:
        if not self.isValidPosition(position):
            error = "Unable to delete card, Position is out of bounds."
            raise ValueError(error)

        return self.listCards()[position-1]

    def length(self) -> int:
        return len(self.listCards())

    def isValidPosition(self, position: int) -> bool:
        return 0 < position <= self.length()

    def incrementAllCardPositionsFrom(self, position: int, increment: int = 1):

        if not self.isValidPosition(position):
            raise ValueError("Provided 'position' value is out of bounds")

        column_id = self.getId()
        tb_card = Card.TABLE_NAME

        new_position = {"position": f"position + {increment}"}

        column_id_match = f"column_id = {column_id}"
        position_is_more_or_equal = f"position >= {position}"

        Database.update(tb_card, _with={"position": new_position},
                        where=f"{column_id_match} AND {position_is_more_or_equal}")

    def insertCard(self, card: Card, position: int):

        if position < 1:
            position = 1

        one_after_last = self.length() + 1
        if position > one_after_last:
            position = one_after_last

        card.setColumnId(self.getId())
        card.setPosition(position)
        card._updateInDatabase()

        self.incrementAllCardPositionsFrom(position)
