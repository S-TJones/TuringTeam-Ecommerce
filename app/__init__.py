from flask import Flask
from .config import Config
from .extensions import db, migrate
from .api import api
from .main import main
from .admin import admin
from .customer import customer
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(admin)
    app.register_blueprint(customer)

    # Flask-Login login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.blueprint_login_views = {
    'main' : '/login'
    }

    return app