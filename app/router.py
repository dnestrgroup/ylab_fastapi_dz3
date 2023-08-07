from fastapi import FastAPI

from app.views.dishes import router as dishes_router
from app.views.menu import router as menu_router
from app.views.sub_menus import router as sub_menu_router


def setup_routes(app: FastAPI) -> None:
    app.include_router(menu_router, prefix='', tags=['Menus'])
    app.include_router(sub_menu_router, prefix='', tags=['Sub Menus'])
    app.include_router(dishes_router, prefix='', tags=['Dishes'])
