import logging
from collections.abc import Callable

from src.image.domain.commands import Command, LoadImage, ProcessImageSource
from src.image.domain.events import Event, ImagePrepared, ImageSaved
from src.image.services.handlers import (
    create_image_view_to_read_model,
    load_image_handler,
    process_image,
    publish_loaded_event,
)
from src.image.services.unit_of_work import AbstractUnitOfWork

logger = logging.getLogger(__name__)

Message = Command | Event


def handle(
    message: Message,
    uow: AbstractUnitOfWork,
) -> None:
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, Event):
            handle_event(message, queue, uow)
        elif isinstance(message, Command):
            handle_command(message, queue, uow)
        else:
            raise Exception(f"{message} не является объектом Event или Command")


def handle_event(
    event: Event,
    queue: list[Message],
    uow: AbstractUnitOfWork,
) -> None:
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            handler(event, uow)
            queue.extend(uow.collect_new_events())
        except Exception as exc:
            logger.exception(f"Ошибка обработки события: {exc} - {event}")
            continue


def handle_command(
    command: Command,
    queue: list[Message],
    uow: AbstractUnitOfWork,
) -> None:
    try:
        handler = COMMAND_HANDLERS[type(command)]
        handler(command, uow)
        queue.extend(uow.collect_new_events())
    except Exception as exc:
        logger.exception(f"Ошибка обработки команды: {exc} - {type(command)}")
        raise


EVENT_HANDLERS: dict[type[Event], list[Callable]] = {
    ImageSaved: [publish_loaded_event],
    ImagePrepared: [create_image_view_to_read_model],
}

COMMAND_HANDLERS: dict[type[Command], Callable] = {
    LoadImage: load_image_handler,
    ProcessImageSource: process_image,
}
