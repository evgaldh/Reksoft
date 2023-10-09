from resourceapp.crud.base_crud import AbstractCrud
from resourceapp import models
from resourceapp import schemas

class ResourceTypeCrud(AbstractCrud):
    def __init__(self) -> None:
        super().__init__(models.ResourceType, schemas.ResourceTypeCreate, schemas.ResourceTypeUpdate, schemas.ResourceType)

resourcetype_crud = ResourceTypeCrud()