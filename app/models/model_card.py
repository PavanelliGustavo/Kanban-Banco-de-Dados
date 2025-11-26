from app.db.database_connection import Database
from datetime import date, datetime
from zoneinfo import ZoneInfo


class Card:

    MAX_DESCRIPTION_LENGTH: int = 1500
    MAX_TITLE_LENGTH: int = 255
    TABLE_CARDS = "tb_card"

    def __init__(self,
                 title: str,
                 description: str,
                 position: int,
                 deadline: date,
                 column_id: int,
                 public_work_id: int) -> None:

        self.setTitle(title)
        self.setDescription(description)
        self.setPosition(position)
        self.setDeadline(deadline)
        self.__setColumnId(column_id)
        self.__setPublicWorkId(public_work_id)
        self.__addToDatabase()

    def __addToDatabase(self):

        if not all(self.getData().values()):
            error = "Failed to add card to database: one or more required values are missing"
            raise RuntimeError(error)

        id = Database.insert(into=self.TABLE_CARDS,
                             data=self.getData(),
                             returning="id")
        if not id:
            raise RuntimeError("Failed to retreive id from SQL insertion.")

        self.__id = int(id)

    def __updateInDatabase(self):
        if not self.getId():
            return
        Database.update(table=self.TABLE_CARDS,
                        _with=self.getData(),
                        where=f"id = {self.__id}")

    def __setColumnId(self, column_id: int):
        if not isinstance(column_id, int):
            raise ValueError("Card column_id must be an integer.")
        if column_id <= 0:
            raise ValueError("Card column_id must be greater than 0.")
        self.__column_id = column_id
        self.__updateInDatabase()

    def __setPublicWorkId(self, public_work_id: int):
        if not isinstance(public_work_id, int):
            raise ValueError("Card public_work_id must be an integer.")
        if public_work_id <= 0:
            raise ValueError("Card public_work_id must be greater than 0.")
        self.__public_work_id = public_work_id

    def setTitle(self, title: str):

        if not isinstance(title, str):
            raise ValueError("Card title must be a string.")

        if len(title) > self.MAX_TITLE_LENGTH:
            error = f"Card title length must be under {self.MAX_TITLE_LENGTH}."
            raise ValueError(error)

        self.__title = title
        self.__updateInDatabase()

    def setDescription(self, description: str):

        if not isinstance(description, str):
            raise ValueError("Card description must be a string.")

        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            error = f"Card description length must be under {self.MAX_DESCRIPTION_LENGTH}."
            raise ValueError(error)

        self.__description = description
        self.__updateInDatabase()

    def setPosition(self, position: int):

        if not isinstance(position, int):
            raise ValueError("Card position must be an integer.")

        if position <= 0:
            raise ValueError("Card position must be greater than 0.")

        self.__position = position
        self.__updateInDatabase()

    def setDeadline(self, deadline: date):
        if not isinstance(deadline, date):
            error = "Card deadline must be an instance of datetime.date."
            raise ValueError(error)
        self.__deadline = deadline
        self.__updateInDatabase()

    def getId(self) -> int:
        return self.__id

    def getData(self) -> dict:
        return {
            "title": self.getTitle(),
            "description": self.getDescription(),
            "position": self.getPosition(),
            "deadline": self.getDeadline(),
            "column_id": self.getColumnId(),
            "public_work_id": self.getPublicWorkId()
        }

    def getTitle(self) -> str:
        return self.__title

    def getDescription(self) -> str:
        return self.__description

    def getPosition(self) -> int:
        return self.__position

    def getDeadline(self) -> date:
        return self.__deadline

    def getColumnId(self) -> int:
        return self.__column_id

    def getPublicWorkId(self) -> int:
        return self.__public_work_id

    def isLate(self) -> bool:
        zone = ZoneInfo("America/Sao_Paulo")
        return datetime.now(zone).date() > self.getDeadline()

    def moveTo(self, column_id: int, position: int):
        self.__setColumnId(column_id)
        self.setPosition(position)

    def incrementPosition(self, increment: int = 1):
        self.setPosition(self.getPosition() + increment)

    def delete(self):
        Database.delete(_from=self.TABLE_CARDS, where=f"id = {self.getId()}")
