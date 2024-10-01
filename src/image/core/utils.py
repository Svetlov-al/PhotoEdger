import os

from src.image.config import IMAGE_FILES_PATH
from src.image.schemas.image_respose_schema import ImageResponseSchema
from src.image.config import config


def add_host_to_images(
    images: list[ImageResponseSchema],
) -> list[ImageResponseSchema]:
    """Добавляет к пути файла текущий активный Host,
    чтобы изображения были доступны в любой среде.
    """

    # Больше выглядит как костыль =)
    URL = f"{config.api_host}:{config.api_port}/api/images"

    for image in images:
        image.image_path = f"{URL}{image.image_path}"
    return images


def get_file_path(file_name: str) -> str:
    # => Определение пути для сохранения изображения в папке /image_files
    image_save_path = f"/{IMAGE_FILES_PATH}"
    os.makedirs(image_save_path, exist_ok=True)

    file_name = f"{file_name.replace(' ', '_')}.jpg"
    file_path = os.path.join(image_save_path, file_name)

    return file_path
