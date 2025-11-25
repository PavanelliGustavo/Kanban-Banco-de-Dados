import os
import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv


class Database:

    @classmethod
    def setUp(cls):

        load_dotenv()
        cls.__postgres_password = os.environ.get("POSTGRES_PASSWORD")

        if cls.__postgres_password is None:
            error = """Ambient variable 'POSTGRES_PASSWORD' is missing, check your '.env' file.
                    For aditional info follow the setup instructions detailed in 'README.md'."""
            raise LookupError(error)

        cls.__createKanbanDatabase()
        cls.__connection = cls.__connectDatabase("kanban_db")
        cls.__cursor = cls.__connection.cursor()

    @classmethod
    def tearDown(cls):
        cls.__cursor.close()
        cls.__connection.close()

    @classmethod
    def __connectDatabase(cls, database_name: str) -> connection:
        try:
            return psycopg2.connect(dbname=database_name, user="postgres",
                                    password=cls.__postgres_password,
                                    host="localhost", port=5432)
        except Exception as e:
            error = f"""Failed to connect to the database. Check if your 'postgres'
                    super-user match the given password in the `.env` file. For
                    aditional info follow the setup instructions detailed in 'README.md'.
                    Original error message: {e}"""
            raise ConnectionError(error)

    @classmethod
    def __createKanbanDatabase(cls):

        connection = cls.__connectDatabase("postgres")
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname='kanban_db'")
        kanban_db_exists = cursor.fetchone()

        if not kanban_db_exists:
            cursor.execute("CREATE DATABASE kanban_db")

        cursor.close()
        connection.close()
