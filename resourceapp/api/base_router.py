import json
from resourceapp.crud.base_crud import AbstractCrud
from resourceapp.db.encoder import ModelEncoder
from resourceapp.db.decoder import ModelDecoder
from resourceapp.schemas.delete_schema import DeleteSchema

class AbstractRouter():
    def __init__(self, crud: AbstractCrud) -> None:
        self.crud : AbstractCrud = crud
        self.methods : dict[str, any] = {
            'GET' : self.handle_get,
            'POST' : self.handle_post,
            'DELETE' : self.handle_delete,
            'PUT': self.handle_put
        }

    def _load_data(self, method, environ):
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        if content_length > 0:
            body = environ['wsgi.input'].read(content_length).decode('utf-8')
            try:
                return json.loads(body, cls=ModelDecoder)
            except Exception:
                self.bad_request("Wrong data format")
        elif method in ['POST', 'PUT', 'DELETE']:
            self.bad_request('Body required')
        return None

    def _process_data(self, method, data):
        if not data:
            return None
        
        schema = None
        if method == 'GET':
            schema = self.crud.filter_schema
        elif method == 'POST':
            schema = self.crud.create_schema
        elif method == 'PUT':
            schema = self.crud.update_schema
        elif method == 'DELETE':
            schema = DeleteSchema

        if schema:
            fields = schema.get_fields()
            filtered_data = {k: data[k] for k in fields if k in data}
            errors = schema.validate(filtered_data)
            if errors:
                self.bad_request(errors)
            return schema(**filtered_data)
        return None

    def handle_request(self, method: str, path_parts: list, environ: dict, start_response):
        """Обрабатывает запрос, пришедший к роутеру ресурса."""
        if method not in self.methods:
            self.not_allowed()
        if len(path_parts) != 0:
            self.not_found()

        data = self._load_data(method, environ)
        if isinstance(data, list):
            self.bad_request("Lists not supported, provide a single value")
        data_instance = self._process_data(method, data)
        return self.methods[method](environ, start_response, data_instance)
        
    def handle_get(self, environ: dict, start_response, data: any):       
        with database_session() as db:
            results = self.crud.get(db, data)
        return self.json_response(results, start_response)
    
    def handle_post(self, environ: dict, start_response, data: any):       
        with database_session() as db:
            result = self.crud.create(db, data)
        return self.json_response(result, start_response)

    def handle_put(self, environ: dict, start_response, data: any):
        with database_session() as db:
            result = self.crud.update(db, data)
        if not result:
            return self.not_found(f'Nothing found with id {str(data.id)}')
        return self.json_response(result, start_response)

    def handle_delete(self, environ: dict, start_response, data: any):
        with database_session() as db:        
            result = self.crud.delete(db, data)
        if not result:
            self.not_found(f'Nothing found with ids {data.ids}')
        return self.json_response(result, start_response)

    def not_found(self, message: str = None):
        raise HTTPError('404 NOT FOUND', message if message else 'Not Found')
    
    def not_allowed(self):
        raise HTTPError('405 METHOD NOT ALLOWED', 'Method Not Allowed')
    
    def bad_request(self, message: str = None):
        raise HTTPError('400 BAD REQUEST', message if message else 'Bad request')
    
    def json_response(self, result: any, start_response):
        if isinstance(result, list):
            response_body = [json.dumps(res, cls=ModelEncoder).encode('utf-8') for res in result]
            response_body = b'\n'.join(response_body)
        else:
            response_body = json.dumps(result, cls=ModelEncoder).encode('utf-8')
        headers = [('Content-Type', 'application/json')]
        start_response('200 OK', headers)
        return [response_body]
    
from resourceapp.core import database_session
from resourceapp.core.exceptions import HTTPError