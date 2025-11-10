from app import db

class ActivityField(db.Model):
    # Model for the 'Activity Field' entity. Relates to Corporate (1,N).

    __tablename__ = 'ActivityField'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Relacionamento com Corporate: ActivityField pode ter N Corporates.
    corporates = db.Relationship('Corporate', blackref='ActivityField', lazy='dynamic')
    # O 'blackref' permite acessar o Activity Field a partir do objeto Corporate

    def __repr__(self):
        return f'<ActivityField {self.id} - {self.name}>'
