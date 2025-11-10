from app import db
from .user import AuthentincatedUser

class Government(AuthentincatedUser):
    # Government model inherits from AutenticatedUser (Joined Table Inheritance)

    __tablename__ = 'Government'

    id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True) # Primary key and Foreign key to the 'User' table

    # Atributos específicos do Governo
    department_name = db.Column(db.String(100), nullable=False)

    # Relacionamentos de Saída -> Government é a "fonte" da FK

    # Government Signs Document (0,N)
    signed_documents = db.relationship('Document', backref='signing_government', lazy='dynamic')
    # A chave estrangeira será armazenada na tabela Document
    ### RELAÇÃO 1:N. A FK TAMBÉM ESTÁ NO DOCUMENT

    # Government Register Public Work (1,N)
    registered_works = db.relationship('PublicWork', backref='registrant_government', lazy='dynamic')
    # lazy='dynamic' permite buscr eficientemente a lista de obras registradas
    ### RELAÇÃO 1:N. A FK ESTÁ NO PUBLICWORK

    # Para o JTI:
    __mapper_args__ = {'polymorphic_identity': 'government'}

    def __repr__(self):
        return f'<Government {self.id} - {self.department_name}>'

