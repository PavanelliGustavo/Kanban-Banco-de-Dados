from datetime import date
from app.models.model_card import Card
from app.models.model_template import Model
from app.models.model_column import Column
from app.models.model_document import Document
from app.models.model_location import Location
from app.db.database_connection import Database
from datetime import date


class PublicWork(Model):

    MAX_TITLE_LENGTH = 255
    MAX_DESCRIPTION_LENGTH = 1500
    TABLE_NAME = "tb_public_work"

    def __init__(self,
                 title: str,
                 start_date: date,
                 location_id: int,
                 government_id: int,
                 corporate_id: int,
                 status: str) -> None:

        self.setTitle(title)
        self.setStatus(status)
        self.__setStartDate(start_date)
        self.__setLocationId(location_id)
        self.__setGovernmentId(government_id)
        self.__setCorporateId(corporate_id)
        self._addToDatabase()

    def setTitle(self, title: str):
        if not isinstance(title, str):
            raise ValueError("Project title must be a string.")

        if len(title) > self.MAX_TITLE_LENGTH:
            error = f"Project title length must be under {self.MAX_TITLE_LENGTH}."
            raise ValueError(error)

        self.__title = title

    def setStatus(self, status: str):
        if not isinstance(status, str):
            raise ValueError("Project status must be a string.")

        if len(status) > self.MAX_DESCRIPTION_LENGTH:
            error = f"Project status length must be under {self.MAX_DESCRIPTION_LENGTH}."
            raise ValueError(error)

        self.__status = status

    def __setStartDate(self, start_date: date):
        if not isinstance(start_date, date):
            raise ValueError("Project start_date must be a date instance.")
        self.__start_date = start_date

    def __setLocationId(self, location_id: int):
        if not isinstance(location_id, int) or location_id <= 0:
            raise ValueError("Location ID must be a positive integer.")
        self.__location_id = location_id

    def __setGovernmentId(self, government_id: int):
        if not isinstance(government_id, int) or government_id <= 0:
            raise ValueError("Government ID must be a positive integer.")
        self.__government_id = government_id

    def __setCorporateId(self, corporate_id: int):
        if not isinstance(corporate_id, int) or corporate_id <= 0:
            raise ValueError("Corporate ID must be a positive integer.")
        self.__corporate_id = corporate_id

    def getTitle(self) -> str:
        return self.__title

    def getStatus(self) -> str:
        return self.__status

    def getStartDate(self) -> date:
        return self.__start_date

    def getLocationId(self) -> int:
        return self.__location_id

    def getGovernmentId(self) -> int:
        return self.__government_id

    def getCorporateId(self) -> int:
        return self.__corporate_id

    def getData(self) -> dict:
        return {
            "title": self.getTitle(),
            "start_date": self.getStartDate(),
            "location_id": self.getLocationId(),
            "government_id": self.getGovernmentId(),
            "corporate_id": self.getCorporateId(),
            "status": self.getStatus()
        }

    @classmethod
    def listByUf(cls, uf: str):

        tb_public_work = cls.TABLE_NAME
        tb_location = Location.TABLE_NAME

        rows = Database.selectInnerJoin(table1=tb_public_work,
                                        table2=tb_location,
                                        on=f"t1.uf = '{uf}'",
                                        columns1=["*"])

        return [PublicWork.instanceFromDatabaseRow(row) for row in rows]

    def listDocuments(self) -> list[Document]:

        tb_documents = Document.TABLE_NAME
        public_work_id_match = f"public_work_id = {self.getId()}"

        rows = Database.select(_from=tb_documents,
                               where=public_work_id_match)

        return [Document.instanceFromDatabaseRow(row) for row in rows]

    def listColumns(self) -> list[Column]:
        tb_column = Column.TABLE_NAME
        public_work_match = f"public_work_id = {self.getId()}"
        rows = Database.select(_from=tb_column, where=public_work_match)
        return [Column.instanceFromDatabaseRow(row) for row in rows]

    def listCards(self) -> list[Card]:
        tb_card = Card.TABLE_NAME
        public_work_match = f"public_work_id = {self.getId()}"
        rows = Database.select(_from=tb_card, where=public_work_match)
        return [Card.instanceFromDatabaseRow(row) for row in rows]

    def getColumnByPosition(self, position: int) -> Column:
        tb_column = Column.TABLE_NAME
        public_work_match = f"column_id = {self.getId()} AND position = {position}"
        row = Database.select(_from=tb_column, where=public_work_match)
        return Column.instanceFromDatabaseRow(row)

    def insertColumn(self, name: str, position: int):

        if position < 1:
            position = 1

        one_after_last = self.length() + 1
        if position > one_after_last:
            position = one_after_last

        Column(name, position, self.getId()).pushDatabase()

    def length(self) -> int:
        return len(self.listColumns())

    def isValidPosition(self, position: int) -> bool:
        return 0 < position <= self.length()
