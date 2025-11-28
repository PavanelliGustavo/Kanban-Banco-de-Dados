from .model_user import AuthenticatedUser
from typing import Any

class Corporate(AuthenticatedUser):

    TABLE_NAME = "Corporate"
    MAX_COMPANY_LENGTH: int = 100
    CNPJ_LENGTH: int = 14
    
    def __init__(self,
                 company_name: str,
                 cnpj: str,
                 field_id: int,
                 email: str,
                 password: str,
                 corp_id: int | None = None):

        super().__init__(email=email,
                         password=password,
                         user_id=corp_id)

        self.setCompanyName(company_name, update_db=False)
        self.setCnpj(cnpj, update_db=False)
        self.setFieldId(field_id, update_db=False)
        
        if corp_id is None:
            self._addToDatabase()
    
    def getData(self) -> dict:
        """ 
        Assume que a ordem das colunas no DB é: company_name, cnpj, field_id, email, password
        """
        data = self._getCommonData()
        data["company_name"] = self.getCompanyName()
        data["cnpj"] = self.getCnpj()
        data["field_id"] = self.getFieldId()
        return data

    @classmethod
    def _fromDatabaseRow(cls, row: tuple) -> 'Corporate':
        
        # Assumindo a ordem id, cnpj, company_name, email, password, field_id
        corp_id, cnpj, company_name, email, password_hash, field_id = row
        
        return cls(corp_id=corp_id, 
                   company_name=company_name, 
                   cnpj=cnpj, 
                   field_id=field_id, 
                   email=email, 
                   password=password_hash)
    
    def setCompanyName(self, company_name: str, update_db: bool = True):
        if not isinstance(company_name, str) or len(company_name.strip()) == 0:
            raise ValueError("Company name must be a non-empty string.")
        if len(company_name) > self.MAX_COMPANY_LENGTH:
            raise ValueError(f"Company name must be under {self.MAX_COMPANY_LENGTH} characters.")
        self.__company_name = company_name
        if self._id and update_db:
            self._updateInDatabase()

    def getCompanyName(self) -> str:
        return self.__company_name

    def setCnpj(self, cnpj: str, update_db: bool = True):
        if not isinstance(cnpj, str) or len(cnpj) != self.CNPJ_LENGTH:
            raise ValueError(f"CNPJ must be a string of length {self.CNPJ_LENGTH}.")
        self.__cnpj = cnpj
        if self._id and update_db:
            self._updateInDatabase()

    def getCnpj(self) -> str:
        return self.__cnpj

    def setFieldId(self, field_id: int, update_db: bool = True):
        if not isinstance(field_id, int) or field_id <= 0:
            raise ValueError("Field ID must be a positive integer.")
        self.__field_id = field_id
        if self._id and update_db:
            self._updateInDatabase()
    
    def getFieldId(self) -> int:
        return self.__field_id
