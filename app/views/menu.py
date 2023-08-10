from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.schemas import CreateMenuRequest, MenuResponse
from app.services.service_menu import MenuService

router = APIRouter()


@router.get('/api/v1/menus', response_model=list[MenuResponse], summary='Метод получения списка меню')
async def get_menus(db: AsyncSession = Depends(get_db)) -> list[MenuResponse]:
    menu_service = MenuService(db=db)
    return await menu_service.get_list()


@router.get('/api/v1/menus/{id}', response_model=MenuResponse)
async def get_menu(id: int, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    menu_service = MenuService(db=db)
    return await menu_service.get_one_menu_by_id(id=id)


@router.patch('/api/v1/menus/{id}', response_model=CreateMenuRequest)
async def patch_menu(id: int, data: CreateMenuRequest, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    menu_service = MenuService(db=db)
    return await menu_service.update_menu(id=id, data=data)


@router.post('/api/v1/menus', response_model=MenuResponse, status_code=201)
async def post_menu(data: CreateMenuRequest, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    menu_service = MenuService(db=db)
    return await menu_service.create_menu(data=data)


@router.delete('/api/v1/menus/{id}')
async def delete_menu(id: int, db: AsyncSession = Depends(get_db)) -> None:
    menu_service = MenuService(db=db)
    return await menu_service.delete_menu(id=id)
