from flask import Flask

from gurella.blueprints.auth import auth_bp
from gurella.error_handlers import handler_bad_request, handler_internal_server_error
from gurella.extensions import init_migrate, db, hashing
from gurella.blueprints.views import views_bp


def create_app(config_name=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    init_extensions(app=app)
    init_blueprints(app=app)
    init_error_handlers(app=app)

    return app


def init_extensions(app):
    db.init_app(app)
    hashing.init_app(app)

    init_migrate(app=app, database=db)


def init_blueprints(app):
    app.register_blueprint(views_bp)
    app.register_blueprint(auth_bp)


def init_error_handlers(app):
    app.register_error_handler(400, handler_bad_request)
    app.register_error_handler(500, handler_internal_server_error)
