from flask import Flask
from .config import Config
from .extensions import db, migrate
from .main import main
from .admin import admin
from .customer import customer
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # db = SQLAlchemy(app)
    # db.init_app(app)
    # migrate.init_app(db, app)

    # Flask-Login login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.blueprint_login_views = {
    'main' : '/login'
    }


    app.register_blueprint(admin)
    app.register_blueprint(customer)

    return app