from app.models.model_user import AuthenticatedUser


class Corporate(AuthenticatedUser):

    TABLE_NAME = "tb_corporate"
    MAX_COMPANY_LENGTH: int = 100
    CNPJ_LENGTH: int = 14

    def __init__(self,
                 company_name: str,
                 cnpj: str,
                 email: str,
                 password: str):

        super().__init__(email=email,
                         password=password)

        self.setCompanyName(company_name)
        self.setCnpj(cnpj)

    def getData(self) -> dict:
        """ 
        Assume que a ordem das colunas no DB é: company_name, cnpj, field_id, email, password
        """
        data = self._getCommonData()
        data["company_name"] = self.getCompanyName()
        data["cnpj"] = self.getCnpj()
        data["field_id"] = self.getFieldId()
        return data

    def setCompanyName(self, company_name: str):
        if not isinstance(company_name, str) or len(company_name.strip()) == 0:
            raise ValueError("Company name must be a non-empty string.")
        if len(company_name) > self.MAX_COMPANY_LENGTH:
            error = f"Company name must be under {self.MAX_COMPANY_LENGTH} characters."
            raise ValueError(error)
        self.__company_name = company_name

    def getCompanyName(self) -> str:
        return self.__company_name

    def setCnpj(self, cnpj: str):
        if not isinstance(cnpj, str) or len(cnpj) != self.CNPJ_LENGTH:
            error = f"CNPJ must be a string of length {self.CNPJ_LENGTH}."
            raise ValueError(error)
        self.__cnpj = cnpj

    def getCnpj(self) -> str:
        return self.__cnpj
