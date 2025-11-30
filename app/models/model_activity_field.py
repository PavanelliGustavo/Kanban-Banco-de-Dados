from app.db.database_connection import Database
from app.models.model_template import Model
from app.models.model_public_work import PublicWork
from app.models.model_corporate_user import Corporate


class ActivityField(Model):

    TABLE_NAME = "tb_field_of_activity"
    MAX_NAME_LENGTH: int = 100

    def __init__(self,
                 name: str) -> None:

        self.setName(name)

    def setName(self, name: str):
        if len(name) == 0:
            raise ValueError("ActivityField name must not be null.")
        if len(name) > self.MAX_NAME_LENGTH:
            error = f"ActivityField name length must be under {self.MAX_NAME_LENGTH}."
            raise (error)
        self.__name = name

    def getData(self) -> dict:
        return {
            "name": self.getName()
        }

    def getName(self) -> str:
        return self.__name

    @classmethod
    def listAll(cls) -> list["ActivityField"]:
        tb_ActivityField = cls.TABLE_NAME
        rows = Database.select(_from=tb_ActivityField)
        return [cls.instanceFromDatabaseRow(row) for row in rows]

    def listPublicWorks(self) -> list[PublicWork]:
        tb_corporate_field_of_activity = "tb_corporate_field_of_activity"
        field_of_activity_match = f"field_of_activity_id = {self.getId()}"
        rows = Database.select(_from=tb_corporate_field_of_activity,
                               where=field_of_activity_match)
        return [PublicWork.instanceFromDatabaseRow(row) for row in rows]

    def listCorporates(self) -> list[Corporate]:
        tb_public_work_field_of_activity = "tb_public_work_field_of_activity"
        field_of_activity_match = f"field_of_activity_id = {self.getId()}"
        rows = Database.select(_from=tb_public_work_field_of_activity,
                               where=field_of_activity_match)
        return [Corporate.instanceFromDatabaseRow(row) for row in rows]
