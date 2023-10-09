import uuid
from resourceapp.db.base import Base
from resourceapp.models.resource_type import ResourceType

class Resource(Base):
    def __init__(self, name : str, current_speed: int, resource_type: ResourceType, id : uuid.UUID = None):
        super().__init__(id)
        self.resource_type : ResourceType = resource_type
        self.name : str = name
        self.current_speed : int = current_speed