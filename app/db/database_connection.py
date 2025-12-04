import logging
import os
from pathlib import Path
from typing import Any
import psycopg2
from psycopg2.extensions import connection, cursor
from psycopg2.errors import DuplicateDatabase
from dotenv import load_dotenv


class Database:

    DB_NAME = "kanban_db"
    MIGRATIONS_DIR = Path("app/sql/migrations")
    CREATE_TABLES_FILE = Path("app/sql/commands/create_tables.sql")

    @classmethod
    def setUp(cls):
        """
        Inicializa a conexão com o banco de dados e garante que o schema/migrações
        estejam aplicados.

        Esta rotina:
        1) Lê a senha do PostgreSQL via variável de ambiente `POSTGRES_PASSWORD`.
        2) Verifica se o banco `kanban_db` existe; se não, cria o banco.
        3) Conecta ao banco e cria `cursor` para operações subsequentes.

        Notes
        -----
        - Este método deve ser chamado antes de qualquer operação de CRUD.

        Raises
        ------
        LookupError
            Caso a variável de ambiente `POSTGRES_PASSWORD` esteja ausente.
        ConnectionError
            Caso a conexão ao banco falhe (credenciais/host/porta incorretos).
        """

        cls.__postgres_password = cls.__getPostgresPassword()

        if not cls.__databaseExists():
            cls.__createDatabase()
        cls.__createTables()

        cls.__connection = cls.__connect(cls.DB_NAME)
        cls.__cursor = cls.__connection.cursor()

    @classmethod
    def tearDown(cls):
        """
        Encerra a conexão e fecha o cursor.

        Notes
        -----
        - Deve ser chamado ao final do ciclo de vida da aplicação.

        Raises
        ------
        psycopg2.Error
            Se ocorrer erro ao fechar cursor ou conexão (situação rara).
        """

        cls.__cursor.close()
        cls.__connection.close()

    @classmethod
    def delete(cls, _from: str, where: str) -> None:
        """
        Remove registros da tabela informada.

        Parameters
        ----------
        _from : str
            Nome da tabela de onde os registros serão removidos.
        where : str
            Condição WHERE para especificar os registros a serem removidos.

        Returns
        -------
        None

        Raises
        ------
        psycopg2.Error
            Se a execução do comando falhar.
        """

        command = f"DELETE FROM {_from} WHERE {where};"
        cls.execute(command)

    @classmethod
    def update(cls, table: str, _with: dict, where: str):
        """
        Atualiza registros de uma tabela com base em um dicionário de colunas/valores.

        Parameters
        ----------
        table : str
            Nome da tabela a ser atualizada.
        _with : dict
            Mapeamento {coluna: valor}.
            Ex.: {"title": "Novo título", "archived": False}
        where : str
            Condição WHERE que restringe os registros a atualizar.
            Ex.: "id = 42" ou "project_id = 7 AND archived = FALSE"

        Returns
        -------
        None

        Notes
        -----
        - Os valores são convertidos para SQL: None => NULL, bool => TRUE/FALSE, numéricos => str.
        - O dicionário `_with` **não pode** ser vazio.

        Raises
        ------
        ValueError
            Se `_with` estiver vazio.
        psycopg2.Error
            Se a execução do comando falhar.
        """
        command = f"UPDATE {table} SET "
        if not _with:
            raise ValueError("O dicionário '_with' não pode ser vazio.")
        values = ", ".join([f"{key} = {cls.__toSQL(value)}"
                            for key, value in _with.items()])
        command += values + f" WHERE {where};"
        cls.execute(command)

    @classmethod
    def insert(cls, into: str, data: dict, returning: str | None = None) -> None | Any:
        """
        Insere um registro na tabela informada.

        Parameters
        ----------
        into : str
            Nome da tabela de destino.
        data : dict
            Mapeamento {coluna: valor}.
            Ex.: {"title": "Nova tarefa", "archived": False, "project_id": 3}
        returning : Optional[str]
            O nome de uma das colunas da tabela selecionada.
            Útil para retornar IDs gerados automaticamente na inserção de um novo registro.

        Returns
        -------
        None | Any
            None se nenhum valor for especificado para returning.
            Any a depender do tipo da coluna selecionada em returning.

        Raises
        ------
        psycopg2.Error
            Se a execução do comando falhar (ex.: violação de constraint).
        """

        cols = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {into} ({cols}) VALUES ({placeholders})"
        if returning:
            query += f" RETURNING {returning}"
        cls.__cursor.execute(query, tuple(data.values()))
        cls.__connection.commit()

        if not returning:
            return

        return_value = cls.__cursor.fetchone()
        if return_value and len(return_value) > 0:
            return return_value[0]

    @classmethod
    def select(cls, _from: str, columns: list[str] | None = None, where: str | None = None) -> list[tuple]:
        """
        Seleciona colunas da tabela informada podendo ou não aplicar restrições com `where`.

        Parameters
        ----------
        _from : str
            Nome da tabela.
        columns : list of str, optional
            Lista de nomes de colunas a serem retornadas. Se `None`, usa `*`.
            Ex.: ["id", "title", "archived"]
        where : str, optional
            Condição WHERE para filtragem.
            Se `None`, retorna todas as linhas.

        Returns
        -------
        list[tuple]
            Linhas retornadas pelo banco. Cada tupla corresponde a uma linha
            e a ordem das colunas segue a consulta.

        Raises
        ------
        psycopg2.Error
            Se a execução do comando falhar.
        """

        cols = ", ".join(columns) if columns else "*"
        query = f"SELECT {cols} FROM {_from}"
        if where:
            query += f" WHERE {where}"
        query += ";"
        cls.__cursor.execute(query)
        return cls.__cursor.fetchall()

    @classmethod
    def selectInnerJoin(cls,
                        table1: str,
                        table2: str,
                        on: str,
                        columns1: list[str] | None = None,
                        columns2: list[str] | None = None,
                        where: str | None = None) -> list[tuple]:
        """
        Executa um SELECT com INNER JOIN entre duas tabelas, com alias `t1` e `t2`.

        Parameters
        ----------
        table1 : str
            Nome da tabela principal (alias `t1`).
        table2 : str
            Nome da segunda tabela (alias `t2`), que será vinculada por INNER JOIN.
        on : str
            Condição ON para o INNER JOIN utilizando os aliases `t1` e `t2`.
        columns1 : list of str, optional
            Colunas de `table1` a retornar. Se `None`, usa `t1.*`.
        columns2 : list of str, optional
            Colunas de `table2` a retornar. Se `None`, usa `t2.*`.
        where : str, optional
            Condição WHERE aplicada ao resultado.
            Ex.: "t2.uf = 'SP'"

        Returns
        -------
        list of tuple
            Linhas retornadas pelo banco.

        Notes
        -----
        - Sempre utilize os aliases (`t1`, `t2`) nos parâmetros `on` e `where`.

        Raises
        ------
        psycopg2.Error
            Se a execução do comando falhar.
        """
        cols1 = cls.__formatColumnsParam(columns1)
        cols2 = cls.__formatColumnsParam(columns2)
        select_cols = cls.__formatColumnsToBeSelected([cols1, cols2])

        query = (f"SELECT {select_cols} "
                 f"FROM {table1} t1 "
                 f"INNER JOIN {table2} t2 ON {on}")

        if where:
            query += f" WHERE {where}"

        cls.__cursor.execute(query)
        return cls.__cursor.fetchall()

    @classmethod
    def selectCrossJoin(cls,
                        table1: str,
                        table2: str,
                        columns1: list[str] | None = None,
                        columns2: list[str] | None = None,
                        where: str | None = None) -> list[tuple]:
        """
        Executa um SELECT com CROSS JOIN entre duas tabelas, com alias `t1` e `t2`.

        Parameters
        ----------
        table1 : str
            Nome da primeira tabela (alias `t1`).
        table2 : str
            Nome da segunda tabela (alias `t2`).
        columns1 : list of str, optional
            Colunas de `table1` a retornar. Se `None`, usa `*`.
            Ex.: ["id", "title"]
        columns2 : list of str, optional
            Colunas de `table2` a retornar. Se `None`, usa `*`.
            Ex.: ["name", "color"]
        where : str, optional
            Condição WHERE aplicada ao resultado do CROSS JOIN.
            Ex.: "t1.project_id = t2.id AND t2.active = TRUE"

        Returns
        -------
        list of tuple
            Linhas retornadas pelo banco.

        Notes
        -----
        - `CROSS JOIN` produz o produto cartesiano; garanta uso de `WHERE` adequado
        para evitar explosão do número de linhas.
        - Ao estruturar o parâmetro `where` certifique-se de utilizar os **alias** (t1, t2)
        e não os nomes das tabelas propriamente. Ex: where="t1.posicao >= t2.posicao"

        Raises
        ------
        psycopg2.Error
            Se a execução do comando falhar.
        """

        cols1 = cls.__formatColumnsParam(columns1)
        cols2 = cls.__formatColumnsParam(columns1)
        selected_cols = cls.__formatColumnsToBeSelected([cols1, cols2])

        query = (f"SELECT {selected_cols} "
                 f"FROM {table1} t1 "
                 f"CROSS JOIN {table2} t2")

        if where:
            query += f" WHERE {where}"

        cls.__cursor.execute(query)
        return cls.__cursor.fetchall()

    @classmethod
    def execute(cls, query: str, *args):
        cls.__cursor.execute(query, *args)
        cls.__connection.commit()

    @classmethod
    def executeFile(cls, path: str):
        cls.__executeSqlFile(cls.__connection, cls.__cursor, Path(path))

    @classmethod
    def __formatColumnsParam(cls, columns: list[str] | None) -> str:
        if columns is not None:
            return ", ".join([f"t1.{c}" for c in columns])
        else:
            return ""

    @classmethod
    def __formatColumnsToBeSelected(cls, columns: list[str]):
        select_cols = ", ".join([col for col in columns if col])
        if not select_cols.strip():
            error = "Unable to perform select. At least one column must be specified"
            raise ValueError(error)
        return select_cols

    @classmethod
    def __toSQL(cls, value: Any) -> str:
        if isinstance(value, bytes):
            return 
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        if isinstance(value, (int, float)):
            return str(value)
        s = str(value).replace("'", "''")
        return f"'{s}'"

    @classmethod
    def __getPostgresPassword(cls):

        load_dotenv()
        password = os.getenv("POSTGRES_PASSWORD")

        if not password:
            raise LookupError("Variável de ambiente 'POSTGRES_PASSWORD' ausente. "
                              "Verifique o arquivo '.env' e siga as instruções do 'README.md'.")
        return password

    @classmethod
    def __connect(cls, db_name: str) -> connection:
        try:
            return psycopg2.connect(dbname=db_name, user="postgres",
                                    password=cls.__postgres_password,
                                    host="localhost", port=5432)
        except Exception as e:
            raise ConnectionError(f"Falha ao conectar ao banco '{db_name}'. "
                                  f"Verifique usuário e senha no arquivo '.env'. Erro original: {e}")

    @classmethod
    def __executeSqlFile(cls, conn: connection, cur: cursor, file_path: Path):
        with file_path.open("r", encoding="utf-8") as file:
            cur.execute(file.read())
        conn.commit()

    @classmethod
    def __executeMigrations(cls, conn: connection, cur: cursor, migrations_dir: Path):
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            cls.__executeSqlFile(conn, cur, migration_file)

    @classmethod
    def __databaseExists(cls) -> bool:
        conn = cls.__connect("postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s",
                    [cls.DB_NAME])
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists

    @classmethod
    def __createDatabase(cls):
        cur = None
        conn = None
        try:
            conn = cls.__connect("postgres")
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE {cls.DB_NAME}")
        except DuplicateDatabase:
            warning = "Attempted to create a database that already exists."
            logging.warning(warning)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def __createTables(cls):
        conn = None
        cur = None
        try:
            conn = cls.__connect(cls.DB_NAME)
            cur = conn.cursor()
            cls.__executeSqlFile(conn, cur, cls.CREATE_TABLES_FILE)
            cls.__executeMigrations(conn, cur, cls.MIGRATIONS_DIR)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
