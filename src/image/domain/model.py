from datetime import datetime

from src.image.domain.events import Event


class Image:
    def __init__(
            self,
            title: str,
            desc: str,
            image_data: bytes,
            created_at: datetime | None = None
    ) -> None:
        self.title = title
        self.description = desc
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.image_data = image_data
        self.events: list[Event] = []

    def __repr__(self):
        return f"<Изображение {self.title}>"

    def __eq__(self, other):
        if not isinstance(other, Image):
            return False
        return other.title == self.title

    def __hash__(self):
        return hash(self.title)

    def __gt__(self, other):
        if self.created_at is None:
            return False
        if other.created_at is None:
            return True
        return self.created_at > other.created_at
