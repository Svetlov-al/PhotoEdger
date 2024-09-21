import json
import logging
from dataclasses import asdict
import redis

from src.image import config
from src.image.domain.events import Event

logger = logging.getLogger(__name__)

r = redis.Redis(**config.get_redis_host_and_port())


def publish(channel, event: Event) -> None:
    """Функция публикации событий в Redis"""
    logging.debug(f"Публикуем событие: Канал={channel}, Событие={event}")
    r.publish(channel, json.dumps(asdict(event)))  # noqa
