import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', '0')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', '1')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', '2')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', '3')


settings = Settings()
