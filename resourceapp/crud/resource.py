from typing import List
from resourceapp.crud.base_crud import AbstractCrud
from resourceapp import models
from resourceapp import schemas
from resourceapp.db.database import DataBase
from resourceapp.schemas.base import BaseSchema

class ResourceCrud(AbstractCrud):
    def __init__(self) -> None:
        super().__init__(
            model=models.Resource,
            create_schema=schemas.ResourceCreate, 
            update_schema=schemas.ResourceUpdate, 
            output_schema=schemas.Resource,
            filter_schema=schemas.ResourceFilter)
        
    def get(self, session: DataBase, data: BaseSchema = None) -> List:
        if not data:
            return super().get(session, data)
        fields = self.output_schema.get_fields()
        columns = ', '.join(fields)
        
        where_clauses = []
        params = []
        
        if data and data.ids:
            ids_placeholders = ', '.join(['%s'] * len(data.ids))
            where_clauses.append(f"resource.id IN ({ids_placeholders})")
            params.extend(data.ids)

        if data and data.type_ids:
            type_ids_placeholders = ', '.join(['%s'] * len(data.type_ids))
            where_clauses.append(f"resource.type_id IN ({type_ids_placeholders})")
            params.extend(data.type_ids)
        
        if data and data.type_names:
            type_names_placeholders = ', '.join(['%s'] * len(data.type_names))
            where_clauses.append(f"resource_type.name IN ({type_names_placeholders})")
            params.extend(data.type_names)
        
        where_clause = ' AND '.join(where_clauses)
        if where_clause:
            where_clause = 'WHERE ' + where_clause

        join_clause = ""
        if data and data.type_names:
            join_clause = "JOIN resource_type ON resource.type_id = resource_type.id"

        query = f'SELECT {columns} FROM resources {join_clause} {where_clause};'
        session.execute_query(query, tuple(params))
        results = session.cursor.fetchall()
        
        return [self.output_schema.from_tuple(row) for row in results]


resource_crud = ResourceCrud()