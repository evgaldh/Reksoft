import json
import uuid

class ModelDecoder(json.JSONDecoder):
    """Сериализатор тела запроса"""
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        for key, value in dct.items():
            try:
                dct[key] = uuid.UUID(value)
            except Exception:
                pass
        return dct