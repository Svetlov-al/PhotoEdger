import json
import logging

import redis

from src.image import config
from src.image.config import REDIS_CHANNEL
from src.image.domain.commands import ProcessImageSource
from src.image.services import messagebus
from src.image.services.unit_of_work import SqlAlchemyUnitOfWork

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


r = redis.Redis(**config.get_redis_host_and_port())


def main():
    """Основная функция запуска вычитки событий из очереди Redis"""
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
    messagebus.handle(cmd, uow=SqlAlchemyUnitOfWork())


if __name__ == "__main__":
    main()
