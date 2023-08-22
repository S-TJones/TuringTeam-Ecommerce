from flask import Flask
from .config import Config
# from .extensions import db, migrate

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    # Initialize SQLAlchemy
    db = SQLAlchemy(app)
    migrate = Migrate(app,db)


    # Flask-Login login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.blueprint_login_views = {
    'main' : '/login'
    }

from .main import main
from .admin import admin
from .customer import customer
app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(customer)


#------The create all should only be executed ONCE---------- 
#running db.create_all() again, it will wipe all your data.

# with app.app_context():
#     # Create database tables
#     db.create_all()

#-----------------------------------------------------------

if __name__ == '__main__':

    
    app.run()