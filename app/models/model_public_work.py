from datetime import date
from app.models.model_activity_field import ActivityField
from app.models.model_template import Model
from app.models.model_card import Card
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
                 description: int,
                 start_date: date,
                 location_id: int,
                 government_id: int,
                 corporate_id: int) -> None:

        self.setTitle(title)
        self.setDescription(description)
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
        self._updateInDatabase()

    def setDescription(self, description: str):
        if not isinstance(description, str):
            raise ValueError("Project description must be a string.")

        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Project description length must be under {self.MAX_DESCRIPTION_LENGTH}."
            )

        self.__description = description
        self._updateInDatabase()

    def __setStartDate(self, start_date: date):
        if not isinstance(start_date, date):
            raise ValueError("Project start_date must be a date instance.")
        self.__start_date = start_date
        self._updateInDatabase()

    def __setLocationId(self, location_id: int):
        if not isinstance(location_id, int) or location_id <= 0:
            raise ValueError("Location ID must be a positive integer.")
        self.__location_id = location_id
        self._updateInDatabase()

    def __setGovernmentId(self, government_id: int):
        if not isinstance(government_id, int) or government_id <= 0:
            raise ValueError("Government ID must be a positive integer.")
        self.__government_id = government_id
        self._updateInDatabase()

    def __setCorporateId(self, corporate_id: int):
        if not isinstance(corporate_id, int) or corporate_id <= 0:
            raise ValueError("Corporate ID must be a positive integer.")
        self.__corporate_id = corporate_id
        self._updateInDatabase()

    def setColumnsList(self, columns_list: list[Card] | None = None):
        self.__columns_list = columns_list if columns_list else []

    def getTitle(self) -> str:
        return self.__title

    def getDescription(self) -> str:
        return self.__description

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
            "description": self.getDescription(),
            "start_date": self.getStartDate(),
            "location_id": self.getLocationId(),
            "government_id": self.getGovernmentId(),
            "corporate_id": self.getCorporateId()
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

    def listActivityFields(self):
        tb_public_work_field_of_activity = "tb_public_work_field_of_activity"
        public_work_match = f"public_work_id = {self.getId()}"
        rows = Database.select(_from=tb_public_work_field_of_activity,
                               where=public_work_match)
        return [ActivityField.instanceFromDatabaseRow(row) for row in rows]

    def getColumnsList(self) -> list[Card]:
        return self.__columns_list

    def getDocumentsList(self) -> list[Document]:

        tb_documents = Document.TABLE_NAME
        public_work_id_match = f"public_work_id = {self.getId()}"

        rows = Database.select(_from=tb_documents,
                               where=public_work_id_match)

        return [Document.instanceFromDatabaseRow(row) for row in rows]

    def insertColumn(self, column: Column, position: int):

        if position < 1:
            position = 1

        one_after_last = self.length() + 1
        if position > one_after_last:
            position = one_after_last

        self.incrementAllColumnPositionsFrom(position)

        columns_list = self.getColumnsList()
        columns_list.insert(position-1, column)

        self.setColumnsList(columns_list)

    def length(self) -> int:
        return len(self.getColumnsList())

    def isValidPosition(self, position: int) -> bool:
        return 0 < position <= self.length()

    def removeColumnAt(self, position: int) -> None:

        if not self.isValidPosition(position):
            error = "Unable to delete card, Position is out of bounds."
            raise ValueError(error)

        self.incrementAllColumnPositionsFrom(position, increment=-1)
        columns_list = self.getColumnsList()

        index = position - 1
        column = columns_list[index]

        columns_list.remove(column)
        self.setColumnsList(columns_list)

        column.delete()

    def incrementAllColumnPositionsFrom(self, position: int, increment: int = 1):

        if not self.isValidPosition(position):
            raise ValueError("Provided 'position' value is out of bounds")

        public_work_id = self.getId()
        tb_column = Column.TABLE_NAME

        new_position = {"position": f"position + {increment}"}

        public_work_id_match = f"public_work_id = {public_work_id}"
        position_is_more_or_equal = f"position >= {position}"

        Database.update(tb_column, _with=new_position,
                        where=f"{public_work_id_match} AND {position_is_more_or_equal}")
