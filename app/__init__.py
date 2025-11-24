from flask import Flask
from os import urandom


def create_app():
    app = Flask(__name__)

    from app.routes.users_login import user_bp
    from app.routes.home_gov import home_gov_bp
    from app.routes.home_corp import home_corp_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(home_gov_bp)
    app.register_blueprint(home_corp_bp)

    app.secret_key = urandom(32)

    return app
