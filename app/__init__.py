from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()

def create_app(config_class='config.Config'):
    # Função de fábrica para criar a instância de aplicação Flask
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Importa as models após inicializar db
    with app.app_context():
        import app.models # executa o app/models/__init__.py
    return app
