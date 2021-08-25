import os

DEBUG = False

SECRET_KEY = os.urandom(24)


DB_USERNAME = 'root'
DB_PASSWORD = '12345678'
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = 'comp3900_db'
DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, db=DB_NAME
)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


basedir = os.path.abspath(os.path.dirname(__file__))

