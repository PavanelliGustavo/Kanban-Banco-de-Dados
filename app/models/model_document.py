from app.db.database_connection import Database
from app.models.model_template import Model
from datetime import date, datetime


class Document(Model):

    MAX_TITLE_LENGTH: int = 255
    MAX_FILE_SIZE_MB: int = 5
    MAX_FILE_SIZE_BYTES: int = 5 * 1024 * 1024
    TABLE_NAME = "tb_document"

    def __init__(self,
                 title: str,
                 file_data: bytes,
                 public_work_id: int,
                 government_id: int,
                 corporate_id: int) -> None:

        self.setTitle(title)
        self.setFileData(file_data)
        self.__setPublicWorkId(public_work_id)
        self.__setGovernmentId(government_id)
        self.__setCorporateId(corporate_id)

    def __setCorporateId(self, corporate_id: int):
        if not isinstance(corporate_id, int):
            raise ValueError("Document corporate_id must be an integer.")
        if corporate_id <= 0:
            raise ValueError("Document corporate_id must be greater than 0.")
        self.__corporate_id = corporate_id

    def __setGovernmentId(self, government_id: int):
        if not isinstance(government_id, int):
            raise ValueError("Document government_id must be an integer.")
        if government_id <= 0:
            raise ValueError("Document government_id must be greater than 0.")
        self.__government_id = government_id

    def __setPublicWorkId(self, public_work_id: int):
        if not isinstance(public_work_id, int):
            raise ValueError("Document public_work_id must be an integer.")
        if public_work_id <= 0:
            raise ValueError("Document public_work_id must be greater than 0.")
        self.__public_work_id = public_work_id

    def setTitle(self, title: str):

        if not isinstance(title, str):
            raise ValueError("Document title must be a string.")

        if len(title) > self.MAX_TITLE_LENGTH:
            error = f"Document title length must be under {self.MAX_TITLE_LENGTH}."
            raise ValueError(error)

        self.__title = title

    def setFileData(self, file_data: bytes):
        if not isinstance(file_data, bytes):
            raise ValueError("Document file_data must be bytes.")

        if len(file_data) == 0:
            raise ValueError("Document file_data cannot be empty.")

        if len(file_data) > self.MAX_FILE_SIZE_BYTES:
            error = (f"Document file_data size ({len(file_data)} bytes) exceeds the limit "
                     f"of {self.MAX_FILE_SIZE_MB}MB ({self.MAX_FILE_SIZE_BYTES} bytes).")
            raise ValueError(error)

        self.__file_data = file_data

    def setUploadDate(self):

        self.__upload_date = datetime.now().date()

    def getData(self) -> dict:
        return {
            "title": self.getTitle(),
            "file_data": self.getFileData(),
            "upload_date": self.getUploadDate(),
            "public_work_id": self.getPublicWorkId(),
            "government_id": self.getGovernmentId(),
            "corporate_id": self.getCorporateId()
        }

    def getTitle(self) -> str:
        return self.__title

    def getFileData(self) -> bytes:
        return self.__file_data

    def getUploadDate(self) -> date:
        return self.__upload_date

    def getPublicWorkId(self) -> int:
        return self.__public_work_id

    def getGovernmentId(self) -> int:
        return self.__government_id

    def getCorporateId(self) -> int:
        return self.__corporate_id
