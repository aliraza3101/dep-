import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # SQLite DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'  # Change it
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Change it