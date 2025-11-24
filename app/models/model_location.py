from app import db

class Location(db.Model):
    # Model para a entidade Location, representado onde a Obra Pública ocorre

    __tablename__ = 'Location'

    id = db.Column(db.Integer, primary_key=True)

    address = db.Column(db.String(250), nullable=False)

    public_work = db.relationship('PublicWork', backref='work_location', uselist=False)

    def __repr__(self):
        return f'<Location {self.id} - {self.address}>'
