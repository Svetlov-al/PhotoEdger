import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.image import views
from src.image.services.unit_of_work import SqlAlchemyUnitOfWork


def create_view_object(
    session: Session,
    image_id: str,
    title: str,
    description: str,
    image_path: str,
    created_at: str,
) -> None:
    query = text(
        """
        INSERT INTO images_view (id, title, description, image_path, created_at)
        VALUES (:id, :title, :description, :image_path, :created_at)
        """
    )

    params = {
        "id": image_id,
        "title": title,
        "description": description,
        "image_path": image_path,
        "created_at": created_at,
    }
    session.execute(query, params)


def test_images_view(sqlite_session_factory) -> None:
    session = sqlite_session_factory()
    uow = SqlAlchemyUnitOfWork(sqlite_session_factory)
    create_view_object(
        session,
        "1",
        "image",
        "desc",
        "image_files/image.jpg",
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    create_view_object(
        session,
        "2",
        "image2",
        "desc",
        "image_files/iamge2.jpg",
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    session.commit()

    assert len(views.images(uow)) == 2


def test_image_by_id_view(sqlite_session_factory) -> None:
    uow = SqlAlchemyUnitOfWork(sqlite_session_factory)
    session = sqlite_session_factory()
    create_view_object(
        session,
        "1",
        "image",
        "desc",
        "image_files/image.jpg",
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    image_in_view = views.image_by_id("1", uow)

    assert image_in_view[0].id == 1
    assert image_in_view[0].title == "image"
    assert image_in_view[0].description == "desc"
    assert image_in_view[0].image_path == "image_files/image.jpg"
