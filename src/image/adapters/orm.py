import logging

from sqlalchemy import Column, DateTime, Integer, LargeBinary, String, Table, event
from sqlalchemy.orm import registry

from src.image.domain.model import Image

mapper_registry = registry()


metadata = mapper_registry.metadata

logger = logging.getLogger(__name__)

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


def start_mappers():
    logger.info("Запуск маппинга таблиц")
    mapper_registry.map_imperatively(Image, images)


# => Подписываемся на события модели Image (Добавляет атрибут events к модели)
@event.listens_for(Image, "load")
def receive_load(image, _) -> None:
    image.events = []
