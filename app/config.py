'''
*********************************************************
this file defines configuration settings for different statges of development.
*********************************************************
'''


import os
from datetime import timedelta
from dotenv import load_dotenv  #load_dotenv reads variables from .env 

load_dotenv()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    #SECRET_KEY is used by Flask to sign session cookies and token securely
    #os.getenv gets the value from .env; if not found, it falls back to the default strung
    SECRET_KEY= os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    #setting DEBUG controls Flask's auto-reloader adn detailed error page
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1")    

    #database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, '..', 'blog.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-super-secret-key-change-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

