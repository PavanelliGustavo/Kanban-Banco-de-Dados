from typing import Iterable
from app.db.database_connection import Database
from abc import ABC, abstractmethod


class Model(ABC):

    """ Classe base para todos os modelos. Depende da implementação apropriada de getData() e da declaração da constante de classe TABLE_NAME."""

    TABLE_NAME: str

    def pushDatabase(self):
        """ Tenta atualizar o registro no banco de dados, se falhar, cria um novo registro
        """
        try:
            self._updateInDatabase()
        except:
            self._addToDatabase()

    def _addToDatabase(self):
        """ Cria um registro no banco de dados com as informações da instância. Deve ser usado apenas uma vez e ao final do construtor da classe que herde de Model.
            É dependente da implementação apropriada de getData()
        """
        if not all(self.getData().values()):
            error = "Failed to add card to database: one or more required values are missing"
            raise RuntimeError(error)

        id = Database.insert(into=self.TABLE_NAME,
                             data=self.getData(),
                             returning="id")
        if not id:
            raise RuntimeError("Failed to retreive id from SQL insertion.")

        self._setId(int(id))

    def _updateInDatabase(self):
        """ Atualiza a linha do banco de dados referente à instância. Serve para sincronizar as informações do BD com as do objeto.
            Deve ser usado ao final de todo método setter.
        """
        if not hasattr(self, "_id"):
            raise RuntimeError("Unable to update, attribute _id is not set")
        Database.update(table=self.TABLE_NAME,
                        _with=self.getData(),
                        where=f"id = {self.getId()}")

    @classmethod
    def instanceFromDatabaseRow(cls, row: list | tuple):
        """Realiza o unpacking de um Iterable (listas, tuplas, etc), ou seja, passa os elementos do Iterable como argumentos individuais
           para o construtor da classe e retorna uma instância.

           Ex: Para um construtor `Construtor(valor1, valor2, valor3, valor4)` poderiamos
           pegar uma `tupla = (a, b, c, d)` e chamar 'Construtor' da seguinte forma `Construtor(*tupla)`, que é equivalente a `Construtor(a, b, c, d)`
        """
        instance = cls(*row[1:])
        instance._setId(row[0])
        return instance

    def delete(self):
        Database.delete(_from=self.TABLE_NAME, where=f"id = {self.getId()}")

    def getId(self) -> int:
        """ Retorna o id da instância """
        return self._id

    def _setId(self, id: int):
        self._id = id

    @classmethod
    def listAll(cls) -> list["Model"]:
        tb = cls.TABLE_NAME
        rows = Database.select(_from=tb)
        return [cls.instanceFromDatabaseRow(row) for row in rows]

    @classmethod
    def getById(cls, id: int) -> "Model":
        attrs = Database.select(_from=cls.TABLE_NAME, where=f"id = {id}")
        attrs = attrs if not isinstance(attrs, Iterable) else attrs[0]
        return cls.instanceFromDatabaseRow(attrs)

    @abstractmethod
    def getData(self) -> dict:
        """ Deve retornar um dicionário cujas chaves são os nomes das colunas da tabela e os valores são os atributos de instância correspondentes.
            Os nomes das colunas devem estar na mesma ordem em que aparecem no banco de dados.

        >>> return {"coluna_1": self.getColuna1(),
                        "coluna_2": self.getColuna2(),
                        "coluna_3": self.getColuna3(),
                        ...}
        """
        pass
