from punq import Container

from src.image.services.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork

container = Container()

container.register(AbstractUnitOfWork, SqlAlchemyUnitOfWork)


def get_uow():
    uow = container.resolve(AbstractUnitOfWork)
    try:
        yield uow
    finally:
        uow.__exit__(None, None, None)
