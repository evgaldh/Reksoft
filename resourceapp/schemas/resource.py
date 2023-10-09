import uuid
from resourceapp.schemas.base import BaseSchema

class ResourceBase(BaseSchema):
    name: str
    max_speed: int

class ResourceUpdate(ResourceBase):
    id: uuid.UUID

class ResourceCreate(ResourceBase):
    pass

class ResourceInDb(ResourceBase):
    id: uuid.UUID

class Resource(ResourceBase):
    pass