import uuid
from resourceapp.schemas.base import BaseSchema

class DeleteSchema(BaseSchema):
    ids: list[uuid.UUID]