from flask import Flask

from .extensions import db
from .routes import main_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-change-me"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///autosalon.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(main_bp)

    with app.app_context():
        from .models import Car, User  # noqa: F401

        db.create_all()

    return app
