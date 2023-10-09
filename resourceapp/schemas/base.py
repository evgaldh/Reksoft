class BaseSchema():
    def __init__(self, *args, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def validate(cls, data: dict):
        errors = []
        annotations = cls.get_annotations()
        for field, expected_type in annotations.items():
            value = data.get(field)

            if not isinstance(value, expected_type):
                errors.append(f"Field '{field}' expected type {expected_type}, got {type(value)}")

            if field not in data:
                errors.append(f"Field '{field}' required")
        return errors
            

    @classmethod
    def get_fields(cls):
        fields = []
        for base in cls.__bases__:
            if hasattr(base, "get_fields"):
                fields.extend(base.get_fields())
        fields.extend(list(cls.__annotations__.keys()))
        return fields

    @classmethod
    def get_annotations(cls):
        annotations = {}
        for base in cls.__bases__:
            if hasattr(base, "get_annotations"):
                annotations.update(base.get_annotations())
        annotations.update(cls.__annotations__)
        return annotations

    @classmethod
    def from_tuple(cls, data_tuple):
        fields = cls.get_fields()
        data_dict = dict(zip(fields, data_tuple))
        return cls(**data_dict)
    
    def to_tuple(self):
        return tuple(getattr(self, field) for field in self.get_fields())