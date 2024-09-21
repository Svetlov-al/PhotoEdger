from src.image.adapters.repository import SqlAlchemyImageRepository
from src.image.domain.model import Image


def test_get_by_title(sqlite_session_factory) -> None:
    session = sqlite_session_factory()
    repo = SqlAlchemyImageRepository(session)
    i1 = Image("image", "description", b"test")
    i2 = Image("image2", "description", b"test")
    repo.add(i1)
    repo.add(i2)

    assert repo.get_by_title("image") == i1
    assert repo.get_by_title("image2") == i2


def test_get_by_image_id(sqlite_session_factory) -> None:
    session = sqlite_session_factory()
    repo = SqlAlchemyImageRepository(session)
    i1 = Image("image", "description", b"test")
    i2 = Image("image2", "description", b"test")
    image_id_1 = repo.add(i1)
    image_id_2 = repo.add(i2)

    assert repo.get(image_id_1) == i1
    assert repo.get(image_id_2) == i2
