from .model_user import AuthenticatedUser
from typing import Any

class Government(AuthenticatedUser):

    TABLE_NAME = "Government"
    MAX_DEPARTMENT_LENGTH: int = 100
    
    def __init__(self,
                 department_name: str,
                 email: str,
                 password: str,
                 gov_id: int | None = None):

        super().__init__(email=email,
                         password=password,
                         user_id=gov_id)
        
        self.setDepartmentName(department_name, update_db=False)

        if gov_id is None:
            self._addToDatabase()
    
    def getData(self) -> dict:
        """ 
        Assume que a ordem das colunas no DB é: department_name, email, password!!!!!!
        """
        data = self._getCommonData()
        data["department_name"] = self.getDepartmentName()
        return data

    @classmethod
    def _fromDatabaseRow(cls, row: tuple) -> 'Government':
        """ Converte uma linha do banco de dados (tupla) em uma instância de Government. """
        
        ''' Assumindo a ordem id, department_name, email, password'''
        gov_id, department_name, email, password_hash = row 
        
        return cls(gov_id=gov_id, 
                   department_name=department_name, 
                   email=email, 
                   password=password_hash)

    
    def setDepartmentName(self, department_name: str, update_db: bool = True):
        if not isinstance(department_name, str) or len(department_name.strip()) == 0:
            raise ValueError("Department name must be a non-empty string.")
        if len(department_name) > self.MAX_DEPARTMENT_LENGTH:
            raise ValueError(f"Department name must be under {self.MAX_DEPARTMENT_LENGTH} characters.")
        self.__department_name = department_name
        if self._id and update_db:
            self._updateInDatabase()

    def getDepartmentName(self) -> str:
        return self.__department_name
