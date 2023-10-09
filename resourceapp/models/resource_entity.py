import uuid
from resourceapp.db.base import Base
from resourceapp.models.resource_type import ResourceType

class Resource(Base):
    def __init__(self, name : str, current_speed: int, type_id: uuid.UUID, id : uuid.UUID = None):
        super().__init__(id)
        self.type_id : uuid.UUID = type_id
        self.name : str = name
        self.current_speed : int = current_speed