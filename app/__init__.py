from flask import Flask
from os import urandom


def create_app():
    app = Flask(__name__)

    from app.routes.users_login import user_bp
    app.register_blueprint(user_bp)
    app.secret_key = urandom(32)

    return app
