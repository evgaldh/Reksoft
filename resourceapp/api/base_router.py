import json
from resourceapp.crud.base_crud import AbstractCrud
from resourceapp.db.encoder import ModelEncoder
from resourceapp.db.decoder import ModelDecoder

class AbstractRouter():
    def __init__(self, crud: AbstractCrud) -> None:
        self.crud : AbstractCrud = crud
        self.methods : dict[str, any] = {
            'GET' : self.handle_get,
            'POST' : self.handle_post,
            'DELETE' : self.handle_delete,
            'PUT': self.handle_put
        }

    def handle_request(self, method: str, path_parts: list, environ: dict, start_response):
        """Обрабатывает запрос, пришедший к роутеру ресурса."""
        if method not in self.methods:
            self.not_allowed()
        if len(path_parts) == 0:
            if method in ['DELETE']:
                self.bad_request('ID is required for this method')
            return self.methods[method](environ, start_response, None)
        elif len(path_parts) == 1:
            id = path_parts.pop(0)
            return self.methods[method](environ, start_response, id)
        else:
            self.not_found()
        
    def handle_get(self, environ: dict, start_response, id : any = None):
        with database_session() as db:
            results = self.crud.get(db, id)
        return self.json_response(results, start_response)
    
    def handle_post(self, environ: dict, start_response, id : any = None):
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        if content_length == 0:
            self.bad_request('Body required')
       
        body = environ['wsgi.input'].read(content_length).decode('utf-8')

        data = json.loads(body)

        fields = self.crud.create_schema.get_fields()
        filtered_data = {k: data[k] for k in fields if k in data}

        errors = self.crud.create_schema.validate(filtered_data)
        if errors:
            self.bad_request(errors)

        instance = self.crud.create_schema(**filtered_data)

        with database_session() as db:
            result = self.crud.create(instance, db)

        return self.json_response(result, start_response)

    def handle_put(self, environ: dict, start_response, id : any = None):
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        if content_length == 0:
            self.bad_request('Body required')

        body = environ['wsgi.input'].read(content_length).decode('utf-8')

        data = json.loads(body, cls=ModelDecoder)

        fields = self.crud.update_schema.get_fields()
        filtered_data = {k: data[k] for k in fields if k in data}

        errors = self.crud.update_schema.validate(filtered_data)
        if errors:
            self.bad_request(errors)

        instance = self.crud.update_schema(**filtered_data)

        with database_session() as db:
            result = self.crud.update(instance, db)
        return self.json_response(result, start_response)

    def handle_delete(self, environ: dict, start_response, id : any):
        with database_session() as db:        
            result = self.crud.delete(id, db)
        if not result:
            self.not_found(f'Nothing found with id {str(id)}')
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