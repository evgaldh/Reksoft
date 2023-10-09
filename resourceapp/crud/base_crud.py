from typing import List, Type
from resourceapp.db.database import DataBase
from resourceapp.db.base import Base
from resourceapp.schemas.base import BaseSchema
import uuid

class AbstractCrud():

    def __init__(
            self, 
            model: Type[Base], 
            create_schema: Type[BaseSchema], 
            update_schema: Type[BaseSchema],
            output_schema: Type[BaseSchema]) -> None:
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.output_schema = output_schema

    def create(self, data: BaseSchema, session: DataBase) -> any:
        fields = data.get_fields()
        placeholders = ', '.join(['%s'] * len(fields))
        columns = ', '.join(fields)
        values = data.to_tuple()
        query = f'INSERT INTO {self.model.__tablename__()} ({columns}) VALUES ({placeholders}) RETURNING *;'
        session.execute_query(query, values)
        session.commit()
        result = session.cursor.fetchone()
        return self.output_schema.from_tuple(result)

    def get(self, session: DataBase, id: uuid.UUID = None) -> List:
        fields = self.output_schema.get_fields()
        columns = ', '.join(fields)
        if id:
            query = f'SELECT {columns} FROM {self.model.__tablename__()} WHERE id = %s;'
            session.execute_query(query, (id,))
            result = session.cursor.fetchone()
            return self.output_schema.from_tuple(result) if result else None
        else:
            query = f'SELECT {columns} FROM {self.model.__tablename__()};'
            session.execute_query(query)
            results = session.cursor.fetchall()
            return [self.output_schema.from_tuple(row) for row in results]

    def update(self, data: BaseSchema, session: DataBase) -> any:
        fields = data.get_fields()
        set_clause = ', '.join([f'{field} = %s' for field in fields if field != "id"])
        values = [getattr(data, field) for field in fields if field != "id"]
        values.append(getattr(data, "id"))
        values_tuple = tuple([str(v) if isinstance(v, uuid.UUID) else v for v in values])
        query = f'UPDATE {self.model.__tablename__()} SET {set_clause} WHERE id = %s RETURNING *;'
        session.execute_query(query, values_tuple)
        session.commit()
        result = session.cursor.fetchone()
        return self.output_schema.from_tuple(result)

    def delete(self, id: uuid.UUID, session: DataBase) -> any:
        fields = self.output_schema.get_fields()
        columns = ', '.join(fields)
        query = f'DELETE FROM {self.model.__tablename__()} WHERE id = %s RETURNING {columns};'
        session.execute_query(query, (id,))
        session.commit()
        result = session.cursor.fetchone()
        return self.output_schema.from_tuple(result)

