from dataclasses import dataclass


class Command:
    pass


@dataclass
class LoadImage(Command):
    title: str
    description: str
    image_source: bytes


@dataclass
class ProcessImageSource(Command):
    image_id: str
