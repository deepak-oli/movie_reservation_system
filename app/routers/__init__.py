from importlib import import_module
from fastapi import FastAPI

router_module_names = ['auth', 'user', 'actor', 'movie']

def include_routers(app: FastAPI):
    for router_module_name in router_module_names:
        router_module = import_module(f'app.routers.{router_module_name}')
        app.include_router(router_module.router)

    return app