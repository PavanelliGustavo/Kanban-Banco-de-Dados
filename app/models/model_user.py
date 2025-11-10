from app import db

class BaseUser(db.Model):
    # Classe base para todos usuários do sistema (Government, Corporate, Civil).

    __abstract__ = True # Indica ao SQLAlchemy que não deve criar uma tabela 'BaseUser'

    id = db.Column(db.Integer, pimary_key=True)
    name = db.Column(db.String(100), nullable=False)

class AutheticatedUser(BaseUser):
    # Superclasse para usuários que precisam de autenticação (Government e Corporate)
    
    __tablename__ = 'User'

    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash =  db.Column(db.String(128), nullable=True)

    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'authenticated',
        'polymorphic_on': type
    }

    def set_password(self, password):
        # Criptografa a senha e a armazena no campo password_hash.
        self.password_hash = generate_password_hash(password)

    def check_password

    def __repr__(self):
        return f'<AutheticatedUser {self.id} - {self.name} - Type: {self.type}>'
    
