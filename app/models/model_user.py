from app.db.database_connection import Database
from app.models.model_template import Model
from werkzeug.security import generate_password_hash, check_password_hash
from abc import abstractmethod
from typing import Any, Optional


class AuthenticatedUser(Model):

    MAX_EMAIL_LENGTH: int = 120

    def __init__(self, email: str, password: str) -> None:

        self.setEmail(email)

        # Apenas verifica se a senha se parece com um hash
        if len(password) > 50 and '$' in password:
            self.__password_hash = password
        else:
            self.setPassword(password)

    def setEmail(self, email: str):
        if not isinstance(email, str) or len(email.strip()) == 0:
            raise ValueError("User email must be a non-empty string.")
        if len(email) > self.MAX_EMAIL_LENGTH:
            raise ValueError(
                f"User email must be under {self.MAX_EMAIL_LENGTH} characters.")
        self.__email = email

    def getEmail(self) -> str:
        return self.__email

    def setPassword(self, password: str):
        self.__password_hash = generate_password_hash(password)

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
            return cls.instanceFromDatabaseRow(results[0])
        return None
