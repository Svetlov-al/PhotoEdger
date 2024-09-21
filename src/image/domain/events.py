from dataclasses import dataclass


class Event:
    pass


@dataclass
class ImageSaved(Event):
    id: int
    title: str
    description: str
    created_at: str


@dataclass
class ImagePrepared(Event):
    id: str
    title: str
    description: str
    image_path: str
    created_at: str
