from .model_user import AuthenticatedUser
from app.db.database_connection import Database

class Government(AuthenticatedUser):

    TABLE_NAME = "Government"
    MAX_DEPARTMENT_LENGTH: int = 100
    
    def __init__(self,
                 name: str,
                 email: str,
                 department_name: str,
                 password: str, # Recebe a senha em texto limpo para gerar o hash
                 gov_id: int | None = None):

        password_hash = generate_password_hash(password)
                     
        super().__init__(user_id=gov_id if gov_id else 0,
                         name=name,
                         email=email,
                         password_hash=password_hash)

        self.setDepartmentName(department_name)
        
        if not gov_id:
            self.__addToDatabase()

    @classmethod
    def getTableName(cls) -> str:
        return cls.TABLE_NAME

    def __addToDatabase(self):
        """ Insere o novo registro na tabela Government. """
        
        data = {
            "department_name": self.getDepartmentName(),
        }
        
        gov_id = self._create(data=data, returning="id")
        self.__id = gov_id

    def __updateInDatabase(self):
        """ Atualiza os atributos na tabela Government. """
        data = {
            "department_name": self.getDepartmentName()
        }
        self._update(data)
    
    def setDepartmentName(self, department_name: str):
        if not isinstance(department_name, str) or len(department_name.strip()) == 0:
            raise ValueError("Department name must be a non-empty string.")
        if len(department_name) > self.MAX_DEPARTMENT_LENGTH:
            raise ValueError(f"Department name must be under {self.MAX_DEPARTMENT_LENGTH} characters.")
        self.__department_name = department_name
        self.__updateInDatabase()

    def getDepartmentName(self) -> str:
        return self.__department_name

    @classmethod
    def findByEmail(cls, email: str) -> 'Government' | None:
        """ Busca e retorna uma instância de Government pelo email. """
        columns = ["id", "name", "email", "password_hash", "department_name"]
        
        result = cls._selectByEmail(email, columns)
        
        if result:
            (gov_id, name, email_val, password_hash, department_name) = result
            return cls(gov_id=gov_id, 
                       name=name, 
                       email=email_val, 
                       department_name=department_name, 
                       password=password_hash)
        return None

    def delete(self):
        Database.delete(_from=self.TABLE_NAME, where=f"id = {self.getId()}")
