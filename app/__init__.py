from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes.routes import login_bp
    app.register_blueprint(login_bp)

    return app
