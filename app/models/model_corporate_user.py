from pathlib import Path
from app.db.database_connection import Database
from app.models.model_public_work import PublicWork
from app.models.model_user import AuthenticatedUser


class Corporate(AuthenticatedUser):

    TABLE_NAME = "tb_corporate"
    MAX_COMPANY_LENGTH: int = 100
    CNPJ_LENGTH: int = 14

    def __init__(self,
                 cnpj: str,
                 company_name: str,
                 email: str,
                 password: str):

        super().__init__(email=email,
                         password=password)

        self.setCompanyName(company_name)
        self.setCnpj(cnpj)

    def getData(self) -> dict:
        data = self._getCommonData()
        data["company_name"] = self.getCompanyName()
        data["cnpj"] = self.getCnpj()
        return data

    def setCompanyName(self, company_name: str):
        if not isinstance(company_name, str) or len(company_name.strip()) == 0:
            raise ValueError("Company name must be a non-empty string.")
        if len(company_name) > self.MAX_COMPANY_LENGTH:
            error = f"Company name must be under {self.MAX_COMPANY_LENGTH} characters."
            raise ValueError(error)
        self.__company_name = company_name

    def getCompanyName(self) -> str:
        return self.__company_name

    def setCnpj(self, cnpj: str):
        if not isinstance(cnpj, str) or len(cnpj) != self.CNPJ_LENGTH:
            error = f"CNPJ must be a string of length {self.CNPJ_LENGTH}. Provided value: {cnpj}"
            raise ValueError(error)
        self.__cnpj = cnpj

    def setActivityFields(self, list_of_ids: list[int]):
        if not isinstance(list_of_ids, list):
            raise ValueError("Invalid value for 'list_of_ids'.")
        if not all(isinstance(_id, int) for _id in list_of_ids):
            raise ValueError("All IDs in 'list_of_ids' must be integers.")
        self.__activity_fields = list_of_ids

    def listPublicWorks(self) -> list[PublicWork]:
        tb_public_work = PublicWork.TABLE_NAME
        corporate_match = f"id = {self.getId()}"
        rows = Database.select(_from=tb_public_work,
                               where=corporate_match)
        return [PublicWork.instanceFromDatabaseRow(row) for row in rows]

    def getCnpj(self) -> str:
        return self.__cnpj

    def pushDatabase(self):
        """ Se for a primeira vez executando, tem que chamar setActivityFields antes """
        try:
            self._updateInDatabase()
        except:
            query = "CALL insert_corporate_with_activity(%s, %s, %s, %s, %s);"
            args = (self.getCnpj(),
                    self.getCompanyName(),
                    self.getEmail(),
                    self.getPasswordHash(),
                    self.__activity_fields)
            Database.execute(query, *args)
