from typing import List
from resourceapp.crud.base_crud import AbstractCrud
from resourceapp import models
from resourceapp import schemas
from resourceapp.db.database import DataBase
from resourceapp.schemas.base import BaseSchema

class ResourceTypeCrud(AbstractCrud):
    def __init__(self) -> None:
        super().__init__(
            model=models.ResourceType,
            create_schema=schemas.ResourceTypeCreate, 
            update_schema=schemas.ResourceTypeUpdate,
            output_schema=schemas.ResourceType,
            filter_schema=schemas.ResourceTypeFilter)
        
    def get(self, session: DataBase, data: BaseSchema = None) -> List:
        if not data:
            return super().get(session, data)
        fields = self.output_schema.get_fields()
        columns = ', '.join(fields)
        
        where_clauses = []
        params = []
        
        if data and data.ids:
            ids_placeholders = ', '.join(['%s'] * len(data.ids))
            where_clauses.append(f"id IN ({ids_placeholders})")
            params.extend(data.ids)
        
        if data and data.names:
            names_placeholders = ', '.join(['%s'] * len(data.names))
            where_clauses.append(f"name IN ({names_placeholders})")
            params.extend(data.names)
        
        where_clause = ' AND '.join(where_clauses)
        if where_clause:
            where_clause = 'WHERE ' + where_clause

        query = f'SELECT {columns} FROM {self.model.__tablename__()} {where_clause};'
        session.execute_query(query, tuple(params))
        results = session.cursor.fetchall()
        return [self.output_schema.from_tuple(row) for row in results]

resourcetype_crud = ResourceTypeCrud()