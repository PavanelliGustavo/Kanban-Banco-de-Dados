from app import db 
from werkzeug.security import generate_password_hash, check_password_hash # Para segurança

class AuthenticatedUser(db.Model):
    
    # Superclasse para todos os usuários que precisam de autenticação (Government e Corporate).
    # Implementa Joined Table Inheritance (Herança de Tabela Agrupada).
    
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) 
    
    # Armazena o tipo de usuário ('government' ou 'corporate')
    type = db.Column(db.String(50)) 

    # --- Argumentos do Mapeador para Herança (JTI) ---
    __mapper_args__ = {
        'polymorphic_identity': 'authenticated',
        'polymorphic_on': type 
    }

    # --- Métodos de Segurança ---
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AuthenticatedUser {self.id} - {self.name} - Type: {self.type}>'
