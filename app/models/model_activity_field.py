from app.models.model_template import Model


class ActivityField(Model):

    TABLE_NAME = "tb_field_of_activity"
    MAX_NAME_LENGTH: int = 100

    def __init__(self,
                 name: str) -> None:

        self.setName(name)

    def setName(self, name: str):
        if len(name) == 0:
            raise ValueError("ActivityField name must not be null.")
        if len(name) > self.MAX_NAME_LENGTH:
            error = f"ActivityField name length must be under {self.MAX_NAME_LENGTH}."
            raise ValueError(error)
        self.__name = name

    def getData(self) -> dict:
        return {
            "name": self.getName()
        }

    def getName(self) -> str:
        return self.__name
