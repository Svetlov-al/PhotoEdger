from pydantic import BaseModel


class ImageResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    created_at: str
    image_path: str
