import os

class Config:
    SECRET_KEY = 'some$3cretKey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pa$$w0rd123@localhost/turingteamecommerce'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = '../uploads'
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
