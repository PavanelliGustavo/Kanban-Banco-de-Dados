from app.db.database_connection import Database
from app.models.model_template import Model
from datetime import date, datetime
from zoneinfo import ZoneInfo


class Document(Model):

    MAX_TITLE_LENGTH: int = 255
    TABLE_NAME = "tb_document"

    def __init__(self,
                 title: str,
                 file_data: bytes,
                 upload_date: date,
                 government_id: int,
                 public_work_id: int,
                 corporate_id: int) -> None:

        self.setTitle(title)
        self.setFileData(position)
        self.setUploadDate(upload_date)
        self.__setGovernmentId(government_id)
        self.__setPublicWorkId(public_work_id)
        self.__setCorporateId(corporate_id)
        self._addToDatabase()

    def __setColumnId(self, column_id: int):
        if not isinstance(column_id, int):
            raise ValueError("Card column_id must be an integer.")
        if column_id <= 0:
            raise ValueError("Card column_id must be greater than 0.")
        self.__column_id = column_id
        self._updateInDatabase()

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
        self._updateInDatabase()

    def setDescription(self, description: str):

        if not isinstance(description, str):
            raise ValueError("Card description must be a string.")

        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            error = f"Card description length must be under {self.MAX_DESCRIPTION_LENGTH}."
            raise ValueError(error)

        self.__description = description
        self._updateInDatabase()

    def setPosition(self, position: int):

        if not isinstance(position, int):
            raise ValueError("Card position must be an integer.")

        if position <= 0:
            raise ValueError("Card position must be greater than 0.")

        self.__position = position
        self._updateInDatabase()

    def setDeadline(self, deadline: date):
        if not isinstance(deadline, date):
            error = "Card deadline must be an instance of datetime.date."
            raise ValueError(error)
        self.__deadline = deadline
        self._updateInDatabase()

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
        Database.delete(_from=self.TABLE_NAME, where=f"id = {self.getId()}")
