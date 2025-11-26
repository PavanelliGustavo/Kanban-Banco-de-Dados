
import os
from pathlib import Path
from typing import Any
import psycopg2
from psycopg2.extensions import connection, cursor
from dotenv import load_dotenv


class Database:

    DB_NAME = "kanban_db"
    MIGRATIONS_DIR = Path("app/sql/migrations")
    CREATE_TABLES_FILE = Path("app/sql/commands/create_tables.sql")

    @classmethod
    def setUp(cls):

        cls.__postgres_password = cls.__getPostgresPassword()

        if not cls.__databaseExists(cls.DB_NAME):
            cls.__createDatabase(cls.DB_NAME)

        cls.__connection = cls.__connect(cls.DB_NAME)
        cls.__cursor = cls.__connection.cursor()

    @classmethod
    def tearDown(cls):
        cls.__cursor.close()
        cls.__connection.close()

    @classmethod
    def delete(cls, table: str, where: str) -> None:
        command = f"DELETE FROM {table} WHERE {where};"
        cls.execute(command)

    @classmethod
    def update(cls, table: str, set: dict, where: str):
        command = f"UPDATE {table} SET "
        if not set:
            raise ValueError("O dicionário 'set' não pode ser vazio.")
        values = ", ".join([f"{key} = {cls.__toSQL(value)}"
                            for key, value in set.items()])
        command += values + f" WHERE {where};"
        cls.execute(command)

    @classmethod
    def insert(cls, table: str, data: dict) -> None:
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        cls.__cursor.execute(query, tuple(data.values()))
        cls.__connection.commit()

    @classmethod
    def select(cls, table: str, columns: list[str] | None = None, where: str | None = None) -> list[tuple]:
        cols = ", ".join(columns) if columns else "*"
        query = f"SELECT {cols} FROM {table}"
        if where:
            query += f" WHERE {where}"
        cls.__cursor.execute(query)
        return cls.__cursor.fetchall()

    @classmethod
    def execute(cls, query: str):
        cls.__cursor.execute(query)
        cls.__connection.commit()

    @classmethod
    def __toSQL(cls, value: Any) -> str:

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
    def __databaseExists(cls, db_name: str) -> bool:
        conn = cls.__connect("postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists

    @classmethod
    def __createDatabase(cls, db_name: str):
        conn = cls.__connect("postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {db_name}")
        cur.close()
        conn.close()

        conn = cls.__connect(db_name)
        cur = conn.cursor()
        cls.__executeSqlFile(conn, cur, cls.CREATE_TABLES_FILE)
        cls.__executeMigrations(conn, cur, cls.MIGRATIONS_DIR)
        cur.close()
        conn.close()
