import os
from dotenv import load_dotenv

load_dotenv()

class ConnectionConfig:
    username_ssh = os.getenv('SSH_USERNAME')
    password = os.getenv('PASSWORD')
    database = os.getenv('DB_NAME')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', "secret")
    APPLICATION_ROOT = os.getenv('APPLICATION_ROOT', "/api")

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = os.getenv('DEBUG', False)