from src.image.schemas.image_respose_schema import ImageResponseSchema
from src.image.services.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy.sql import text


def images(uow: SqlAlchemyUnitOfWork) -> list[ImageResponseSchema]:
    """Получаем список всех обработанных изображений"""
    with uow:
        query = text(
            """
            SELECT id, title, description, created_at, image_path FROM images_view
        """
        )
        results = uow.session.execute(query)
        results = results.mappings().all()

        if not results:
            return []

        return [ImageResponseSchema(**result) for result in results]


def image_by_id(
    image_id: str, uow: SqlAlchemyUnitOfWork
) -> list[ImageResponseSchema]:
    """
    Получаем изображение по его ID
    image_id должен быть str (Модель полностью в строковом варианте)
    """
    with uow:
        query = text(
            """
            SELECT id, title, description, created_at, image_path 
            FROM images_view 
            WHERE id = :image_id
            """
        )
        result = uow.session.execute(query, {"image_id": image_id})

        result_list = [dict(row) for row in result.mappings()]

        if not result_list:
            return []

        return [ImageResponseSchema(**r) for r in result_list]
