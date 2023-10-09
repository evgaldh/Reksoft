from resourceapp.crud.base_crud import AbstractCrud
from resourceapp import models
from resourceapp import schemas

class ResourceCrud(AbstractCrud):
    def __init__(self) -> None:
        super().__init__(models.Resource, schemas.ResourceCreate, schemas.ResourceUpdate, schemas.Resource)

resource_crud = ResourceCrud()