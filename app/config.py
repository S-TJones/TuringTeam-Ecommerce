import os

class Config:
    SECRET_KEY = 'some$3cretKey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/turingdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # WTF_CSRF_CHECK_DEFAULT=False
    WTF_CSRF_ENABLED = False
    # UPLOAD_FOLDER = '../uploads'
    UPLOAD_FOLDER = '/uploads/'
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
