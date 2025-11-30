from app.models.model_user import AuthenticatedUser


class Government(AuthenticatedUser):

    TABLE_NAME = "tb_government"
    MAX_DEPARTMENT_LENGTH: int = 100

    def __init__(self,
                 department_name: str,
                 email: str,
                 password: str) -> None:

        super().__init__(email=email,
                         password=password)

        self.setDepartmentName(department_name)

    def getData(self) -> dict:
        """ 
        Assume que a ordem das colunas no DB é: department_name, email, password!!!!!!
        """
        data = self._getCommonData()
        data["department_name"] = self.getDepartmentName()
        return data

    def setDepartmentName(self, department_name: str):
        if not isinstance(department_name, str) or len(department_name.strip()) == 0:
            raise ValueError("Department name must be a non-empty string.")
        if len(department_name) > self.MAX_DEPARTMENT_LENGTH:
            raise ValueError(
                f"Department name must be under {self.MAX_DEPARTMENT_LENGTH} characters.")
        self.__department_name = department_name

    def getDepartmentName(self) -> str:
        return self.__department_name
