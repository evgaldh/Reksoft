from resourceapp.core.exceptions import HTTPError
from resourceapp.api.base_router import AbstractRouter

class AppRouter:
    def __init__(self) -> None:
        """Главный роутер приложения"""
        self.routers : dict[str, AbstractRouter] = {}

    def add(self, path : str, router: AbstractRouter):
        """Регистрация дополнительных роутеров и эндпоинтов, им соответсвующих"""
        self.routers[path] = router

    def route_request(self, method: str, path: str, environ: dict, start_response):
        """Перенаправление запроса отвественному за эндпоинт роутеру"""
        path_parts = path.strip('/').split('/')
        router_name = path_parts.pop(0)
        router = self.routers.get(router_name)

        if router:
            return router.handle_request(method, path_parts, environ, start_response)
        else:
            self.not_found()


    def not_found(self):
        """Обработчик ошибки 404"""
        raise HTTPError('404 NOT FOUND', 'Not Found')