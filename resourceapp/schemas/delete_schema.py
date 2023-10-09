import uuid
from resourceapp.schemas.base import BaseSchema

class DeleteSchema(BaseSchema):
    """Схема для поддержки множественного удаления"""
    ids: list[uuid.UUID]