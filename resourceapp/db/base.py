class Base:
    def __init__(self, id: any = None) -> None:
        self.id = id

    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()