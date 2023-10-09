import uuid
from typing import Optional
from resourceapp.schemas.base import BaseSchema

class ResourceBase(BaseSchema):
    name: str
    current_speed: int
    type_id: uuid.UUID

class ResourceUpdate(ResourceBase):
    id: uuid.UUID

class ResourceCreate(ResourceBase):
    pass

class ResourceInDb(ResourceBase):
    id: uuid.UUID

class Resource(ResourceInDb):
    speed_excess: float

class ResourceFilter(BaseSchema):
    ids: Optional[list[uuid.UUID]] = None
    type_ids: Optional[list[uuid.UUID]] = None
    type_names: Optional[list[str]] = None