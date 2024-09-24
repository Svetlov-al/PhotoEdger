import logging

from sqlalchemy import text

from src.image.core.utils import get_file_path
from src.image.exceptions.description_to_long_exception import (
    DescriptionToLongException,
)
from src.image.exceptions.image_not_found_exception import ImageNotFoundException
from src.image.services.add_text_to_image import add_text_to_image
from src.image.services.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from src.image.adapters import redis_eventpublisher
from src.image.config import REDIS_CHANNEL
from src.image.domain.commands import LoadImage, ProcessImageSource
from src.image.domain.events import ImagePrepared, ImageSaved
from src.image.domain.model import Image
from src.image.exceptions.image_already_loaded_exception import ImageAlreadyLoaded

logger = logging.getLogger(__name__)


def load_image_handler(
    cmd: LoadImage,
    uow: AbstractUnitOfWork,
) -> int:
    """Хендлер загрузки и сохранения изображения в основную модель базы."""
    with uow:
        image = uow.images.get_by_title(title=cmd.title)

        # => Валидириуем модель изображения на дубликат и длину описания
        # (В целом данная проверка опциональная, и можно добавлять к изображению временную метку
        # и отвязаться от нейминга этих изображений)
        if image:
            logger.info(
                "Попытка повторной загрузки изображения",
                extra={
                    "title": image.title,
                    "created_at": image.created_at,
                    "description": image.description,
                },
            )
            raise ImageAlreadyLoaded(
                f"Изображение с таким названием уже сохранено {image.title}"
            )

        if len(cmd.description) > 200:
            logger.info(
                "Попытка загрузки изображения с слишком длинным описанием",
                extra={"title": cmd.title, "description": cmd.description},
            )
            raise DescriptionToLongException(
                "Описание превышает допустимое значение в 200 знаков."
            )

        image = Image(
            title=cmd.title,
            desc=cmd.description,
            image_data=cmd.image_source,
            created_at=None,
        )
        image_id = uow.images.add(image)

        # => После успешного сохранения объекта в базе, создаем событие на отправку изображения в Redis
        # для дальнейшей обработки и сохранения в модель представления
        image.events.append(
            ImageSaved(
                id=image_id,
                title=image.title,
                description=image.description,
                created_at=image.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            )
        )

        logger.info(
            "Создано событие",
            extra={
                "event": type(ImageSaved),
                "title": image.title,
            },
        )

        uow.commit()

        return image_id


def process_image(
    cmd: ProcessImageSource,
    uow: AbstractUnitOfWork,
) -> None:
    """Хендлер обработки изображения, добавляет черную полосу к изображению с текстом
    содержащим описание изображения.
    """
    with uow:
        image = uow.images.get(image_id=int(cmd.image_id))

        if not image:
            raise ImageNotFoundException(
                f"Изображение с ID: {cmd.image_id} не найдено"
            )

        # => Получает путь к файлу по его названию
        # (Возможно путь сохраняется не самым оптимальным путем, по причине возможной смены папки
        # для хранения изображения, и следовало бы отвязаться от этой настройки)
        file_path = get_file_path(file_name=image.title)

        # => Добавляем текст к изображению и сохраняем на диск
        add_text_to_image(
            image_data=image.image_data,
            file_path=file_path,
            text=image.description,
        )

        # => Создаем новое событие, что изображение готово к сохранению в модель представления.
        image.events.append(
            ImagePrepared(
                id=image.id,  # type: ignore
                title=image.title,
                description=image.description,
                image_path=file_path,
                created_at=image.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            )
        )
        uow.commit()


def publish_loaded_event(
    event: ImageSaved,
    uow: AbstractUnitOfWork,  # noqa
) -> None:
    """Хендлер отправки события в очередь Redis"""
    redis_eventpublisher.publish(REDIS_CHANNEL, event)


def create_image_view_to_read_model(
    event: ImagePrepared,
    uow: SqlAlchemyUnitOfWork,
) -> None:
    """Хендлер сохранения изображения в модель представления"""
    with uow:
        query = text(
            """
            INSERT INTO images_view (id, title, description, image_path, created_at)
            VALUES (:id, :title, :description, :image_path, :created_at)
            """
        )

        params = {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "image_path": event.image_path,
            "created_at": event.created_at,
        }
        uow.session.execute(query, params)

        uow.commit()
