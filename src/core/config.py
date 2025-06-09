from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Config(BaseSettings):
    APP_NAME: str = "master-pol"
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000

    BD_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SQLALCHEMY_ECHO: bool = False

    @property
    def POSTGRES_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


config = Config()
