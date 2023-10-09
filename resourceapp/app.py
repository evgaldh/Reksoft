import json
import traceback
import logging
from resourceapp.api import resourcetype_router, resource_router
from resourceapp.core import database_session
from resourceapp.core import AppRouter, HTTPError, settings

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
if settings.DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

def initialize_database():
    with database_session() as db:
        db.apply_migrations()

initialize_database()

main_router = AppRouter()
main_router.add('resources', resource_router)
main_router.add('resourcetypes', resourcetype_router)

def application(environ : dict, start_response):
    try:
        method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
        logger.debug(f"Received {method} request on {path}")
        response = main_router.route_request(method, path, environ, start_response)
        logger.debug(f"Processed {method} request on {path} successfully")
        return response
    except HTTPError as e:
        logger.error("HTTPError encountered: %s", e)
        start_response(e.status, [('Content-Type', 'application/json')])
        error_message = {'message': e.message if e.message else 'Error message is empty.'}
        return [json.dumps(error_message).encode('utf-8')]
    except Exception as e:
        logger.exception("Unexpected server error: %s", e)
        start_response('500 Internal server error', [('Content-Type', 'application/json')])
        if settings.DEBUG:
            error_trace = traceback.format_exc()
            error_message = {
                'message': 'Unexpected server error', 
                'details': str(e), 
                'trace': error_trace.splitlines()
            }
        else:
            error_message = {
                'message': 'Unexpected server error'
            }
        return [json.dumps(error_message).encode('utf-8')]