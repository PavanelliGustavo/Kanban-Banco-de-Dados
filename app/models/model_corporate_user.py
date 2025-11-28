from .model_user import AuthenticatedUser
from app.db.database_connection import Database

class Corporate(AuthenticatedUser):

    TABLE_NAME = "Corporate"
    MAX_COMPANY_LENGTH: int = 100
    CNPJ_LENGTH: int = 14
    
    def __init__(self,
                 name: str,
                 email: str,
                 company_name: str,
                 cnpj: str,
                 field_id: int,
                 password: str,
                 corp_id: int | None = None):

        password_hash = generate_password_hash(password)
        
        super().__init__(user_id=corp_id if corp_id else 0,
                         name=name,
                         email=email,
                         password_hash=password_hash)

        self.setCompanyName(company_name)
        self.setCnpj(cnpj)
        self.__setFieldId(field_id)
        
        if not corp_id:
            self.__addToDatabase()

    @classmethod
    def getTableName(cls) -> str:
        return cls.TABLE_NAME
    
    def __addToDatabase(self):
        """ Insere o novo registro na tabela Corporate. """
        
        data = {
            "company_name": self.getCompanyName(),
            "cnpj": self.getCnpj(),
            "field_id": self.getFieldId(),
        }
        
        corp_id = self._create(data=data, returning="id")
        self.__id = corp_id 

    def __updateInDatabase(self):
        """ Atualiza os atributos na tabela Corporate. """
        data = {
            "company_name": self.getCompanyName(),
            "cnpj": self.getCnpj(),
            "field_id": self.getFieldId(),
        }
        self._update(data)

    def setCompanyName(self, company_name: str):
        if not isinstance(company_name, str) or len(company_name.strip()) == 0:
            raise ValueError("Company name must be a non-empty string.")
        if len(company_name) > self.MAX_COMPANY_LENGTH:
            raise ValueError(f"Company name must be under {self.MAX_COMPANY_LENGTH} characters.")
        self.__company_name = company_name
        self.__updateInDatabase()

    def setCnpj(self, cnpj: str):
        if not isinstance(cnpj, str) or len(cnpj) != self.CNPJ_LENGTH:
            raise ValueError(f"CNPJ must be a string of length {self.CNPJ_LENGTH}.")
        # Adicionar validação de formato de CNPJ aqui!!!!
        self.__cnpj = cnpj
        self.__updateInDatabase()

    def __setFieldId(self, field_id: int):
        if not isinstance(field_id, int) or field_id <= 0:
            raise ValueError("Field ID must be a positive integer.")
        self.__field_id = field_id
        self.__updateInDatabase()
    
    def getCompanyName(self) -> str:
        return self.__company_name

    def getCnpj(self) -> str:
        return self.__cnpj
    
    def getFieldId(self) -> int:
        return self.__field_id
    
    @classmethod
    def findByEmail(cls, email: str) -> 'Corporate' | None:
        columns = ["id", "name", "email", "password_hash", "company_name", "cnpj", "field_id"]
        
        result = cls._selectByEmail(email, columns)
        
        if result:
            (corp_id, name, email_val, password_hash, company_name, cnpj, field_id) = result
            
            return cls(corp_id=corp_id, 
                       name=name, 
                       email=email_val, 
                       company_name=company_name, 
                       cnpj=cnpj, 
                       field_id=field_id, 
                       password=password_hash)
        return None

    def delete(self):
        Database.delete(_from=self.TABLE_NAME, where=f"id = {self.getId()}")
