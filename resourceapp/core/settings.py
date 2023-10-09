import os

class Settings:
    DB_NAME: str = os.environ.get('DB_NAME', 'resource_app') 
    DB_USER: str = os.environ.get('DB_USER') 
    DB_PASSWORD: str = os.environ.get('DB_PASSWORD') 
    DB_HOST: str = os.environ.get('DB_HOST', 'localhost') 
    DB_PORT: str = os.environ.get('DB_PORT', '5432')

    DEBUG: bool = os.environ.get('DEBUG', 'False').lower() == 'true'

    def __init__(self) -> None:
        self._check_required_vars()    

    def _check_required_vars(self):
        required_vars = ["DB_USER", "DB_PASSWORD"]
        missing_vars = [var for var in required_vars if not getattr(self, var)]
        if missing_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")


settings = Settings()