# Configuration settings for Flask Car Dealership App
import os
from dotenv import load_dotenv

load_dotenv()


DEBUG = True
SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")