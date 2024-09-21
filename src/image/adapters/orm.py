from sqlalchemy import (
    DateTime,
    LargeBinary,
    Table,
    MetaData,
    Column,
    Integer,
    String,
    create_engine,
    event,
)
from sqlalchemy.orm import registry

from src.image.config import get_postgres_uri
from src.image.domain.model import Image

metadata = MetaData()

mapper_registry = registry()

images = Table(
    "images",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("description", String(255), nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("image_data", LargeBinary, nullable=False),
)

images_view = Table(
    "images_view",
    metadata,
    Column("id", String(255)),
    Column("title", String(255)),
    Column("description", String(255)),
    Column("image_path", String(255)),
    Column("created_at", String(255)),
)


# => Подписываемся на события модели Image (Добавляет атрибут events к модели)
@event.listens_for(Image, "load")
def receive_load(image, _) -> None:
    image.events = []


def start_mappers():
    mapper_registry.map_imperatively(Image, images)


engine = create_engine(get_postgres_uri())
metadata.create_all(engine)

start_mappers()
