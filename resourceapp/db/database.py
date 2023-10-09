import psycopg2
import os

class DataBase:
    def __init__(
            self,
            dbname: str = None, 
            user: str = None, 
            password: str = None, 
            host='localhost', 
            port='5432'
        ) -> None:
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dsn = f"dbname={self.dbname} user={self.user} password={self.password} host={self.host} port={self.port}"
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(self.dsn)
        #self.connection.autocommit = True 
        self.cursor = self.connection.cursor()

    def create_database(self):
        conn = psycopg2.connect(dbname="postgres", user=self.user, password=self.password, host=self.host, port=self.port)
        conn.autocommit = True 
        cur = conn.cursor()
        
        cur.execute(f"CREATE DATABASE {self.dbname} OWNER {self.user};")
        
        cur.close()
        conn.close()

    def apply_migrations(self):
        self.execute_query('select max(version) from database_version;')
        current_version = self.cursor.fetchone()[0]
        new_version = None
        migrations_path = os.path.join(os.getcwd(), 'migrations')
        for migration_file in sorted(os.listdir(migrations_path)):
            migration_file_version = int(migration_file.split('_')[0])
            if current_version and current_version >= migration_file_version:
                continue
            migration_file_path = os.path.join(migrations_path, migration_file)
            with open(migration_file_path, 'r') as file:
                sql = file.read()
                self.execute_query(sql)
                new_version = migration_file_version

        if new_version:
            self.execute_query(f'UPDATE database_version SET version = {new_version}')
            if self.cursor.rowcount == 0:
                self.execute_query(f'INSERT INTO database_version (version) VALUES ({new_version})')
            
        self.commit()

    def ensure_database_exists(self):
        try:
            self.connect()
        except psycopg2.OperationalError:
            self.create_database()
            self.connect()

    def ensure_version_table_exists(self):
        self.connect()
        
        check_table_query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'database_version'
        );
        """
        
        self.execute_query(check_table_query)
        table_exists = self.cursor.fetchone()[0]

        if not table_exists:
            create_table_query = """
            CREATE TABLE database_version (
                version INTEGER PRIMARY KEY
            );
            """
            self.execute_query(create_table_query)
            self.commit()

    def execute_query(self, query: str, params: any = None):
        try:
            self.cursor.execute(query, params)
        except Exception as e:
            self.rollback()
            raise e
        
    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def __enter__(self):
        self.ensure_database_exists()
        self.ensure_version_table_exists()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connection.close()