from resourceapp.api.base_router import AbstractRouter
from resourceapp.crud import resource_crud

class ResourceRouter(AbstractRouter):
    def __init__(self) -> None:
        super().__init__(resource_crud)

resource_router = ResourceRouter()