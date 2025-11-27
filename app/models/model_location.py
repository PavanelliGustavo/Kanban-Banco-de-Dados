from app.db.database_connection import Database
from app.models.model_template import Model

class Location(Model):
    # Model para a entidade Location, representado onde a Obra Pública ocorre

    TABLE_NAME = "Location"

    id = db.Column(db.Integer, primary_key=True)

    address = db.Column(db.String(250), nullable=False)

    public_work = db.relationship('PublicWork', backref='work_location', uselist=False)

    def __repr__(self):
        return f'<Location {self.id} - {self.address}>'

