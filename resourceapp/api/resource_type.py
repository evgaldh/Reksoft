from resourceapp.api.base_router import AbstractRouter
from resourceapp.crud import resourcetype_crud

class ResourceTypeRouter(AbstractRouter):

    def __init__(self) -> None:
        super().__init__(resourcetype_crud)

resourcetype_router = ResourceTypeRouter() 