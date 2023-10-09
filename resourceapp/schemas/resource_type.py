import uuid
from resourceapp.schemas.base import BaseSchema

class ResourceTypeBase(BaseSchema):
    name: str
    max_speed: int

class ResourceTypeUpdate(ResourceTypeBase):
    id: uuid.UUID

class ResourceTypeCreate(ResourceTypeBase):
    pass

class ResourceTypeInDb(ResourceTypeBase):
    id: uuid.UUID

class ResourceType(ResourceTypeInDb):
    pass