from fastapi import APIRouter, HTTPException, Request, status

from src.image.core.utils import add_host_to_images
from src.image.schemas.image_respose_schema import ImageResponseSchema
from src.image import views
from src.image.services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter()


@router.get(
    "/images",
    response_model=list[ImageResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получение списка обработанных изображений"
)
def images_view(request: Request) -> list[ImageResponseSchema]:
    """Представление для получения списка всех обработанных изображений."""

    result = views.images(SqlAlchemyUnitOfWork())

    return add_host_to_images(result, str(request.url))


@router.get(
    "/images/{image_id}",
    response_model=list[ImageResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получение изображения по его ID"
)
def image_view(request: Request, image_id: int) -> list[ImageResponseSchema]:
    """Представление для получения изображения по его ID"""

    result = views.image_by_id(str(image_id), SqlAlchemyUnitOfWork())

    if not result:
        raise HTTPException(status_code=404, detail=f"Изображение с ID: {image_id} не найдено.")

    return add_host_to_images(result, str(request.url))
