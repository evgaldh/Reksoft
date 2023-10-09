import json
import uuid
from resourceapp.schemas.base import BaseSchema

class ModelEncoder(json.JSONEncoder):
    """Сериализатор тела ответа"""
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, BaseSchema):
            return obj.__dict__
        return super().default(obj)