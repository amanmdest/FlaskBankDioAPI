import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound

from src.models.base import Base


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///dio_bank.sqlite',
        JWT_SECRET_KEY='super-secret',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize extension
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)

    # register blueprints
    from src.controllers import auth, role, user, account, transfer

    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    app.register_blueprint(user.app)
    app.register_blueprint(account.app)
    app.register_blueprint(transfer.app)

    @app.errorhandler(NotFound)
    def handle_404_error(e):
        return {"message": "The requested resource was not found"}, 404

    return app
