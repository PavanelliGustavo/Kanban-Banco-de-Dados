from app.db.database_connection import Database
from app.models.model_template import Model
from app.models.model_public_work import PublicWork


class Location(Model):

    TABLE_NAME = "tb_location"
    MAX_ADDRESS_LENGTH = 255
    MAX_CITY_LENGTH = 50
    VALID_FEDERAL_UNITS = [
        "AC", "AL", "AP", "AM", "BA", "CE",
        "DF", "ES", "GO", "MA", "MT", "MS",
        "MG", "PA", "PB", "PR", "PE", "PI",
        "RJ", "RN", "RS", "RO", "RR", "SC",
        "SP", "SE", "TO"
    ]

    def __init__(self, uf: str, city: str, address: str, ):
        self.__setUf(uf)
        self.__setCity(city)
        self.__setAddress(address)

    def __setUf(self, uf: str):
        if not uf in self.VALID_FEDERAL_UNITS:
            raise ValueError("Ivalid UF")
        self.__uf = uf

    def __setCity(self, city):
        if not isinstance(city, str):
            raise ValueError("Location's city must be a string")
        if len(city) > self.MAX_CITY_LENGTH:
            error = f"Location's city length must be under {self.MAX_CITY_LENGTH}."
            raise ValueError(error)
        self.__city = city

    def __setAddress(self, address: str):

        if not isinstance(address, str):
            raise ValueError("Location's address must be a string.")

        if len(address) > self.MAX_ADDRESS_LENGTH:
            error = f"Location address length must be under {self.MAX_ADDRESS_LENGTH}."
            raise ValueError(error)

        self.__address = address

    def getUf(self):
        return self.__uf

    def getCity(self):
        return self.__city

    def getAddress(self):
        return self.__address

    def getData(self):
        return {"address": self.getAddress()}

    def listPublicWorks(self) -> list[PublicWork]:
        tb_public_work = PublicWork.TABLE_NAME
        location_match = f"id = {self.getId()}"
        rows = Database.select(_from=tb_public_work,
                               where=location_match)
        return [PublicWork.instanceFromDatabaseRow(row) for row in rows]
