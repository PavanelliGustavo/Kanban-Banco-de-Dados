from app import db
from .user import AutheticatedUser

class Corporate(AutheticatedUser):
    # Model for the 'Corporate' entity. Responsável por assinar documentos e gerenciar 
    # o Kanban (Columns e Cards) da obra.
    # Herda de AuthenticatedUser (Joined Table Inheritance)

    __tablename__ = 'Corporate'

    id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True) # Primary key and Foreign key
    company_name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)

    # Corporate Signs Document (0,N)
    signed_documents = db.relationship('Document', backref='signing_corporate', lazy='dynamic')
    # A FK está em Document

    # Corporate Updates PublicWork (0,N)
    managed_works = db.relationship('PublicWork', backref='managing_corporate', lazy='dynamic')
    # A FK está em PublicWork

    # Corporate Creates/Updates Column (0,N)
    updated_columns = db.relationship('Column', backref='updater_corporate', lazy='dynamic')
    # A FK está em Column

    # Corporate Creates/Updates Card (0,N)
    updated_cards = db.relationship('Card', backref='updater_corporate', lazy='dynamic')
    # A FK está em Card

    # Paro o JTI:
    __mapper_args__ = {'polymorphic_identity': 'corporate'}

    def __repr__(self):
        return f'<Corporate {self.id} - {self.company_name}>'
