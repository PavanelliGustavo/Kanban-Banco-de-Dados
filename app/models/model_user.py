from app.db.database_connection import Database
from werkzeug.security import generate_password_hash, check_password_hash
from abc import ABC, abstractmethod
from typing import Any

class AuthenticatedUser(ABC):
    MAX_NAME_LENGTH: int = 100
    MAX_EMAIL_LENGTH: int = 120
    
    def __init__(self, user_id: int, name: str, email: str, password_hash: str) -> None:
        
        self.__id = user_id
        self.setName(name)
        self.setEmail(email)
        self.__password_hash = password_hash
    
    @classmethod
    @abstractmethod
    def getTableName(cls) -> str:
        pass
    
    def setName(self, name: str):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("User name must be a non-empty string.")
        if len(name) > self.MAX_NAME_LENGTH:
            raise ValueError(f"User name must be under {self.MAX_NAME_LENGTH} characters.")
        self.__name = name
    
    def setEmail(self, email: str):
        # Simplificação: Apenas verifica o tipo e o tamanho máximo
        if not isinstance(email, str) or len(email.strip()) == 0:
            raise ValueError("User email must be a non-empty string.")
        if len(email) > self.MAX_EMAIL_LENGTH:
            raise ValueError(f"User email must be under {self.MAX_EMAIL_LENGTH} characters.")
        self.__email = email

    def setPassword(self, password: str):
        """ Gera o hash da senha para armazenamento seguro. """
        self.__password_hash = generate_password_hash(password)
    
    def getId(self) -> int:
        return self.__id

    def getName(self) -> str:
        return self.__name

    def getEmail(self) -> str:
        return self.__email
    
    def getPasswordHash(self) -> str:
        return self.__password_hash

    
    
    def checkPassword(self, password: str) -> bool:
        return check_password_hash(self.getPasswordHash(), password)

    
    def _create(self, data: dict, returning: str = 'id') -> int:
        data['name'] = self.getName()
        data['email'] = self.getEmail()
        data['password_hash'] = self.getPasswordHash()

        new_id = Database.insert(into=self.getTableName(),
                                 data=data,
                                 returning=returning)
        if not new_id:
             raise RuntimeError(f"Failed to retrieve {returning} from SQL insertion in {self.getTableName()}.")
        
        self.__id = int(new_id)
        return self.__id

    def _update(self, data: dict, where: str | None = None):
        """ Método base para atualização no banco de dados pelas classes filhas. """
        if not self.getId():
            return
        
        data['name'] = self.getName()
        data['email'] = self.getEmail()
        
        if 'password_hash' in data:
            del data['password_hash']

        where_clause = where if where else f"id = {self.getId()}"
        
        Database.update(table=self.getTableName(),
                        _with=data,
                        where=where_clause)
        
    @classmethod
    def _selectByEmail(cls, email: str, columns: list[str] | None = None) -> tuple[Any, ...] | None:
        """ Método base para buscar usuário pelo email. """
        results = Database.select(
            _from=cls.getTableName(),
            columns=columns,
            where=f"email = '{email}'"
        )
        return results[0] if results else None
