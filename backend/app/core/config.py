import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    # Database
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_CONTAINER_NAME: str
    DB_PORT: int

    # Hashing
    PWD_ALGORYTHM: str
    ALGORYTHM: str
    SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
    )

    @property
    def ASYNC_DATABASE_DSN(self) -> PostgresDsn:  # pylint: disable=C0103
        db_name = f"{self.DB_NAME}_test" if os.getenv("TESTING") else self.DB_NAME
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{db_name}"


settings = Settings()
