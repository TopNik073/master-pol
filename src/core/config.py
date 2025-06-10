from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, SecretStr

from pathlib import Path


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SENSITIVE_DATA: list[str] = ["password", "name"]

    APP_NAME: str = "master-pol"
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    DEBUG: bool = False

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SQLALCHEMY_ECHO: bool = False

    @property
    def POSTGRES_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = (
        "%(asctime)s | %(levelname)-8s | %(name)s | "
        "[%(filename)s:%(funcName)s:%(lineno)d] - %(message)s"
    )
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    _LOGS_DIR: Path = BASE_DIR / "logs"

    @property
    def LOGS_DIR(self) -> Path:
        Path.mkdir(self._LOGS_DIR, parents=True, exist_ok=True)
        return self._LOGS_DIR

    JWT_SECRET: SecretStr
    ACCESS_TOKEN_EXP_MIN: int = 30
    REFRESH_TOKEN_EXP_MIN: int = 30 * 24 * 60


config = Config()
