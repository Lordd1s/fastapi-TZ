import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    DB_ECHO: bool = os.getenv('DB_ECHO')


settings = Settings()
