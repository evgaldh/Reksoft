import uuid
from typing import Union, List, get_origin, get_args
NoneType = type(None)

class BaseSchema():
    def __init__(self, *args, **kwargs) -> None:
        """Первоначальная схема с функциями валидации"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def _validate_value_type(cls, value, expected_type):
        origin = get_origin(expected_type)
        args = get_args(expected_type)

        # Если ожидается Union (включая Optional)
        if origin == Union:
            if value is None:
                return NoneType in args
            return any(cls._validate_value_type(value, subtype) for subtype in args)

        # Если ожидается список
        elif origin == list:
            if not isinstance(value, list):
                return False
            item_type = args[0]
            if item_type == uuid.UUID:  # Частный случай для UUID
                return all(cls._is_uuid(item) for item in value)
            return all(isinstance(item, item_type) for item in value)

        # Для обычных типов
        else:
            return isinstance(value, expected_type or origin)

    @staticmethod
    def _is_uuid(value):
        try:
            uuid.UUID(str(value))
            return True
        except ValueError:
            return False


    @classmethod
    def validate(cls, data: dict):
        errors = []
        annotations = cls.get_annotations()

        for field, expected_type in annotations.items():
            value = data.get(field, None)  # Получить значение, если оно есть

            if not cls._validate_value_type(value, expected_type):
                errors.append(f"Field '{field}' expected type {expected_type}, got {type(value)}")

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

