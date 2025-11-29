from app.db.database_connection import Database
from app.models.model_template import Model
from werkzeug.security import generate_password_hash, check_password_hash
from abc import abstractmethod
from typing import Any, Optional


class AuthenticatedUser(Model):

    MAX_EMAIL_LENGTH: int = 120

    def __init__(self, email: str, password: str, user_id: int | None = None) -> None:

        self._id = user_id if user_id is not None else 0

        self.setEmail(email, update_db=False)

        # Apenas verifica se a senha se parece com um hash
        if len(password) > 50 and '$' in password:
            self.__password_hash = password
        else:
            self.setPassword(password, update_db=False)

    def setEmail(self, email: str, update_db: bool = True):
        if not isinstance(email, str) or len(email.strip()) == 0:
            raise ValueError("User email must be a non-empty string.")
        if len(email) > self.MAX_EMAIL_LENGTH:
            raise ValueError(
                f"User email must be under {self.MAX_EMAIL_LENGTH} characters.")
        self.__email = email
        if self._id and update_db:
            self._updateInDatabase()

    def getEmail(self) -> str:
        return self.__email

    def setPassword(self, password: str, update_db: bool = True):
        self.__password_hash = generate_password_hash(password)
        if self._id and update_db:
            self._updateInDatabase()

    def getPasswordHash(self) -> str:
        return self.__password_hash

    def checkPassword(self, password: str) -> bool:
        return check_password_hash(self.getPasswordHash(), password)

    def _getCommonData(self) -> dict:
        return {
            "email": self.getEmail(),
            "password": self.getPasswordHash(),
        }

    @classmethod
    def findByEmail(cls, email: str) -> Optional['AuthenticatedUser']:
        results = Database.select(
            _from=cls.TABLE_NAME,
            where=f"email = '{email}'"
        )

        if results:
            return cls._fromDatabaseRow(results[0])
        return None

    @classmethod
    @abstractmethod
    def _fromDatabaseRow(cls, row: tuple) -> 'AuthenticatedUser':
        # Converte uma linha do banco de dados (tupla) em uma instância da classe
        pass
