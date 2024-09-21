from abc import ABC, abstractmethod

from sqlalchemy import insert
from sqlalchemy.orm import Session

from src.image.adapters.orm import images
from src.image.domain.model import Image


class AbstractRepository(ABC):
    def __init__(self):
        self.seen: set[Image] = set()

    def add(self, image: Image) -> int:
        image_id = self._add(image)
        self.seen.add(image)

        return image_id

    def get(self, image_id: int) -> Image:
        image = self._get(image_id)
        if image:
            self.seen.add(image)
        return image

    def get_by_title(self, title: str) -> Image:
        image = self._get_by_title(title)
        if image:
            self.seen.add(image)
        return image

    @abstractmethod
    def _add(self, image: Image) -> int:
        raise NotImplementedError

    @abstractmethod
    def _get(self, image_id: int) -> Image:
        raise NotImplementedError

    @abstractmethod
    def _get_by_title(self, title: str) -> Image:
        raise NotImplementedError


class SqlAlchemyImageRepository(AbstractRepository):
    """Репозиторий для работы с моделью Image"""

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def _add(self, image: Image) -> int:
        db_image = {
            "title": image.title,
            "description": image.description,
            "created_at": image.created_at,
            "image_data": image.image_data,
        }

        stmt = insert(images).values(**db_image).returning(images.c.id)
        res = self.session.execute(stmt)

        return res.scalar_one()

    def _get(self, image_id: int) -> Image | None:
        return self.session.query(Image).filter_by(id=image_id).first()

    def _get_by_title(self, title: str) -> Image | None:
        return self.session.query(Image).filter_by(title=title).first()
