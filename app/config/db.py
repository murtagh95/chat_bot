"""Config of DB"""
from pydantic import Field

from app.config.base import BaseSettings
from app.config.cfg import IS_TEST

BASE_DB_MODELS = "app.core.models.tortoise"
DB_MODELS = [
    f"{BASE_DB_MODELS}.business",
    f"{BASE_DB_MODELS}.product",
    f"{BASE_DB_MODELS}.job",
    f"{BASE_DB_MODELS}.user",
    f"{BASE_DB_MODELS}.message",
    f"{BASE_DB_MODELS}.card",
    f"{BASE_DB_MODELS}.button",
    f"{BASE_DB_MODELS}.way"
]
POSTGRES_DB_URL = "postgres://{postgres_user}:{postgres_password}@" \
                  "{postgres_host}:{postgres_port}/{postgres_db}"
SQLITE_DB_URL = "sqlite://:memory:"


class PostgresSettings(BaseSettings):
    """Postgres env values"""

    postgres_user: str = Field("postgres", env="POSTGRES_USER")
    postgres_password: str = Field("postgres", env="POSTGRES_PASSWORD")
    postgres_db: str = Field("mydb", env="POSTGRES_DB")
    postgres_port: str = Field("5432", env="POSTGRES_PORT")
    postgres_host: str = Field("postgres", env="POSTGRES_HOST")


class TortoiseSettings(BaseSettings):
    """Tortoise-ORM settings"""

    db_url: str
    modules: dict
    generate_schemas: bool

    @classmethod
    def generate(cls):
        """Generate Tortoise-ORM settings (with sqlite if tests)"""

        if IS_TEST:
            db_url = SQLITE_DB_URL
        else:
            postgres = PostgresSettings()
            db_url = POSTGRES_DB_URL.format(**postgres.dict())
            del postgres
        modules = {"models": DB_MODELS}
        return TortoiseSettings(
            db_url=db_url,
            modules=modules,
            generate_schemas=True
        )
