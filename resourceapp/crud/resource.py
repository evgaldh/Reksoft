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
        fields = self.output_schema.get_fields()
        columns = ', '.join([f'resource.{field}' for field in fields if field != 'speed_excess'])
        
        speed_excess = """
        CASE 
            WHEN resource.current_speed > resourcetype.max_speed THEN
                (resource.current_speed - resourcetype.max_speed) * 100 / resourcetype.max_speed
            ELSE
                0
        END AS speed_excess_percentage
        """

        columns = f"{columns}, {speed_excess}"

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
            where_clauses.append(f"resourcetype.name IN ({type_names_placeholders})")
            params.extend(data.type_names)
        
        where_clause = ' AND '.join(where_clauses)
        if where_clause:
            where_clause = 'WHERE ' + where_clause

        join_clause = "JOIN resourcetype ON resource.type_id = resourcetype.id"

        query = f'SELECT {columns} FROM resource {join_clause} {where_clause};'
        session.execute_query(query, tuple(params))
        results = session.cursor.fetchall()
        
        return [self.output_schema.from_tuple(row) for row in results]


resource_crud = ResourceCrud()