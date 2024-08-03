import os

class Config:
    SECRET_KEY = 'f8d83e7f7b4c4c872e5a2f1d1e7e3b2f'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = '19d92e1e58b6c7f10e3c3f3b2e54f6b7'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # Token expiration in seconds
