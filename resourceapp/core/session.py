from resourceapp.db import DataBase

def database_session():
    return DataBase(
        dbname=settings.DB_NAME, 
        user=settings.DB_USER, 
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT
        )

from resourceapp.core.settings import settings