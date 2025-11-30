from app.models.model_activity_field import ActivityField
from app.models.model_corporate_user import Corporate
from app.models.model_relational_template import Relational


class CorporateActivityField(Relational):

    TABLE_NAME = "tb_corporate_field_of_activity"

    @classmethod
    def listCorporatesWith(cls, activity_field: ActivityField) -> list[Corporate]:
        return cls.listMatching("field_of_activity_id",
                                activity_field.getId(),
                                Corporate)

    def listActivityFieldsFrom(cls, corporate: Corporate) -> list[ActivityField]:
        return cls.listMatching("corporate_id",
                                corporate.getId(),
                                ActivityField)
