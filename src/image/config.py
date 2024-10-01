from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    api_host: str = Field(alias="API_HOST", default="localhost")
    api_port: int = Field(alias="API_PORT", default=8000)

    redis_host: str = Field(alias="REDIS_HOST", default="localhost")
    redis_port: int = Field(alias="REDIS_POST", default=6379)

    db_host: str = Field(alias="DB_HOST", default="localhost")
    db_port: int = Field(alias="PORT", default=5432)
    db_user: str = Field(alias="DB_USER", default="postgres")
    db_name: str = Field(alias="DB_NAME", default="image")
    db_password: str = Field(alias="DB_PASSWORD", default="password")
    redis_channel: str = Field(alias="REDIS_CHANNELL", default="image_saved")
    image_files_path: str = Field(alias="IMAGE_FILES_PATH", default="image_files")


config: Config = Config()


def get_postgres_uri() -> str:
    return f"postgresql://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}"


def get_api_url() -> str:
    return f"http://{config.api_host}:{config.api_port}"  # noqa


def get_redis_host_and_port() -> dict:
    return dict(host=config.redis_host, port=config.redis_port)


REDIS_CHANNEL = "image_saved"

IMAGE_FILES_PATH = "image_files"
