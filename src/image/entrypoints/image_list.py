import logging

from fastapi import APIRouter, Depends, HTTPException, status

from src.image import views
from src.image.core.init import get_uow
from src.image.core.utils import add_host_to_images
from src.image.schemas.image_respose_schema import ImageResponseSchema
from src.image.services.unit_of_work import AbstractUnitOfWork

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/images",
    response_model=list[ImageResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получение списка обработанных изображений",
)
def images_view(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> list[ImageResponseSchema]:
    """Представление для получения списка всех обработанных изображений."""

    result = views.images(uow)

    return add_host_to_images(result)


@router.get(
    "/images/{image_id}",
    response_model=list[ImageResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получение изображения по его ID",
)
def image_view(
    image_id: int, uow: AbstractUnitOfWork = Depends(get_uow)
) -> list[ImageResponseSchema]:
    """Представление для получения изображения по его ID"""

    result = views.image_by_id(str(image_id), uow)

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Изображение с ID: {image_id} не найдено."
        )

    return add_host_to_images(result)
