from unittest import mock

import pytest

from src.image.adapters.repository import AbstractRepository
from src.image.config import IMAGE_FILES_PATH
from src.image.core.utils import get_file_path
from src.image.domain import commands
from src.image.domain.model import Image
from src.image.exceptions.description_to_long_exception import (
    DescriptionToLongException,
)
from src.image.exceptions.image_already_loaded_exception import ImageAlreadyLoaded
from src.image.services import messagebus
from src.image.services.unit_of_work import AbstractUnitOfWork


class FakeRepository(AbstractRepository):
    def __init__(self, images):
        super().__init__()
        self._images = set(images)

    def _add(self, image: Image) -> int:
        self._images.add(image)
        image.id = len(self._images)
        return image.id

    def _get(self, image_id):
        return next((i for i in self._images if i.id == image_id), None)

    def _get_by_title(self, title: str):
        return next((i for i in self._images if i.title == title), None)


class FakeSession:
    def execute(self, *args, **kwargs) -> None:  # noqa
        return None


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.images = FakeRepository([])
        self.committed = False
        self.session = FakeSession()  # type: ignore

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


@pytest.fixture(autouse=True)
def fake_redis_publish():
    with mock.patch("src.image.adapters.redis_eventpublisher.publish"):
        yield


class TestAddImage:
    def test_for_new_image(self) -> None:
        uow = FakeUnitOfWork()
        messagebus.handle(commands.LoadImage("image", "description", b"test"), uow)

        assert uow.images.get(1) is not None
        assert uow.committed

    def test_already_existing_image(self) -> None:
        uow = FakeUnitOfWork()
        messagebus.handle(commands.LoadImage("image", "description", b"test"), uow)

        with pytest.raises(ImageAlreadyLoaded):
            messagebus.handle(
                commands.LoadImage("image", "description", b"test"), uow
            )

    def test_to_long_description(self) -> None:
        with pytest.raises(DescriptionToLongException):
            uow = FakeUnitOfWork()
            messagebus.handle(
                commands.LoadImage("image", f"{'d' * 201}", b"test"), uow
            )

    @mock.patch("src.image.services.handlers.add_text_to_image")
    def test_process_image(self, mock_add_text) -> None:
        mock_add_text.return_value = None

        uow = FakeUnitOfWork()
        image_id = uow.images.add(Image("image", "description", b"test"))

        messagebus.handle(commands.ProcessImageSource(image_id=str(image_id)), uow)

        assert uow.committed
        mock_add_text.assert_called_once()

    def test_get_file_path(self) -> None:
        image = Image("image", "description", b"test")
        file_path = get_file_path(file_name=image.title)

        assert f"/{IMAGE_FILES_PATH}/{image.title}.jpg" == file_path
