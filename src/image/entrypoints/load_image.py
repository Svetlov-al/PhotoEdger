import logging

from fastapi import APIRouter, File, Form, UploadFile, status
from fastapi.responses import JSONResponse

from src.image.domain.commands import LoadImage
from src.image.exceptions.description_to_long_exception import (
    DescriptionToLongException,
)
from src.image.exceptions.image_already_loaded_exception import ImageAlreadyLoaded
from src.image.services import messagebus

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/images",
    status_code=status.HTTP_201_CREATED,
    summary="Загрузка изображения",
)
async def load_image(
    title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)
) -> JSONResponse:
    """Представление для загрузки изображения в модель"""

    # => Получаем данные в байтах
    image_data = await file.read()

    try:
        cmd = LoadImage(title=title, description=description, image_source=image_data)
        results = messagebus.handle(cmd)
        image_id = results.pop(0)
    except (ImageAlreadyLoaded, DescriptionToLongException) as exc:
        return JSONResponse(
            {"message": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse(
        {"success": True, "image_id": image_id}, status_code=status.HTTP_201_CREATED
    )
