import uuid
from resourceapp.db.base import Base

class ResourceType(Base):
    """Тип ресурса"""
    def __init__(self, name: str, max_speed: int, id: uuid.UUID = None) -> None:
        super().__init__(id)
        self.name : str = name
        self.max_speed : int = max_speed
