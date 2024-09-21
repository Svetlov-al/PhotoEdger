import os

from src.image.config import IMAGE_FILES_PATH
from src.image.schemas.image_respose_schema import ImageResponseSchema


def add_host_to_images(
    images: list[ImageResponseSchema], host: str
) -> list[ImageResponseSchema]:
    """Добавляет к пути файла текущий активный Host,
    чтобы изображения были доступны в любой среде.
    """

    # Больше выглядит как костыль =)
    for image in images:
        image.image_path = f"{host}{image.image_path}"
    return images


def get_file_path(file_name: str) -> str:
    # => Определение пути для сохранения изображения в папке /image_files
    image_save_path = f"/{IMAGE_FILES_PATH}"
    os.makedirs(image_save_path, exist_ok=True)

    file_name = f"{file_name.replace(' ', '_')}.jpg"
    file_path = os.path.join(image_save_path, file_name)

    return file_path
