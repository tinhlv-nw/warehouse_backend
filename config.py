import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mhvslzqkhosting_user:n0tpUblIc@luatthienxung.com/mhvslzqkhosting_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Secret key cho Flask
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Secret key cho JWT
