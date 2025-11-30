from app.models.model_activity_field import ActivityField
from app.models.model_public_work import PublicWork
from app.models.model_relational_template import Relational


class PublicWorkActivityField(Relational):

    TABLE_NAME = "tb_public_work_field_of_activity"

    @classmethod
    def listPublicWorksWith(cls, activity_field: ActivityField) -> list[PublicWork]:
        return cls.listMatching("field_of_activity_id",
                                activity_field.getId(),
                                PublicWork)

    def listActivityFieldsFrom(cls, public_work: PublicWork) -> list[ActivityField]:
        return cls.listMatching("public_work_id",
                                public_work.getId(),
                                ActivityField)
