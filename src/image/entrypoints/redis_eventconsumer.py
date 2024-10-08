import json
import logging

import redis

from src.image import config
from src.image.adapters.orm import start_mappers
from src.image.config import REDIS_CHANNEL
from src.image.domain.commands import ProcessImageSource
from src.image.exceptions.image_not_found_exception import ImageNotFoundException
from src.image.services import messagebus
from src.image.services.unit_of_work import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


r = redis.Redis(**config.get_redis_host_and_port())


def main():
    """Основная функция запуска вычитки событий из очереди Redis"""
    logger.info("Redis pubsub запущен!")

    start_mappers()

    pubsub = r.pubsub(ignore_subscribe_messages=True)

    # => Подписываемся на канал получения событий на сохранение и обработку изображений.
    pubsub.subscribe(REDIS_CHANNEL)

    # => Вычитываем события и запускаем обработку
    for m in pubsub.listen():
        handle_process_image(m)


def handle_process_image(m) -> None:
    """Обработчик сообщений полученных из Redis"""
    logging.info(f"Начинаю обработку сообщения {m}")
    data = json.loads(m["data"])

    # => Создаем команду на обработку изображения и отправляем в шину сообщений
    cmd = ProcessImageSource(image_id=data["id"])
    try:
        messagebus.handle(cmd, uow=SqlAlchemyUnitOfWork())
    except ImageNotFoundException:
        logger.critical(
            f"Попытка обработки изображения с несуществующим ID: {cmd.image_id}"
        )


if __name__ == "__main__":
    main()
