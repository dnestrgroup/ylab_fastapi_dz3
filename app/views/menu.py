import json

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.redis.redis import redis_client
from app.db.repositorie_for_menu import RepositoriesMenus
from app.schemas.schemas import CreateMenuRequest, MenuResponse

router = APIRouter()


@router.get('/api/v1/menus', response_model=list[MenuResponse], summary='Метод получения списка меню')
async def get_menus(db: AsyncSession = Depends(get_db)) -> list[MenuResponse]:
    cached_data = redis_client.get('/api/v1/menus')
    if cached_data:
        menus = json.loads(cached_data)
        return [MenuResponse(**json.loads(menu)) for menu in menus]
    repo = RepositoriesMenus(db)
    menus = await repo.get_list()
    menus_for_redis = [menu.json() for menu in menus]
    redis_client.setex('/api/v1/menus', 1000, json.dumps(menus_for_redis))
    return menus


@router.get('/api/v1/menus/{id}', response_model=MenuResponse)
async def get_menu(id: int, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    cached_data = redis_client.get('/api/v1/menus/' + str(id))
    if cached_data:
        return MenuResponse(**json.loads(cached_data))
    repo = RepositoriesMenus(db)
    menu = await repo.get(id=id)
    if menu:
        redis_client.setex('/api/v1/menus/' + str(id), 1000, menu.json())
        return menu
    raise HTTPException(status_code=404, detail='menu not found')


@router.patch('/api/v1/menus/{id}', response_model=CreateMenuRequest)
async def patch_menu(id: int, data: CreateMenuRequest, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    repo = RepositoriesMenus(db)
    update_menu = await repo.update(id=id, data=data)
    redis_client.flushall()
    return MenuResponse(id=update_menu.id, title=update_menu.title, description=update_menu.description)


@router.post('/api/v1/menus', response_model=MenuResponse, status_code=201)
async def post_menu(data: CreateMenuRequest, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    repo = RepositoriesMenus(db)
    new_menu = await repo.create(data=data)
    redis_client.flushall()
    return MenuResponse(id=new_menu.id, title=new_menu.title, description=new_menu.description)


@router.delete('/api/v1/menus/{id}')
async def delete_menu(id: int, db: AsyncSession = Depends(get_db)) -> None:
    repo = RepositoriesMenus(db)
    await repo.delete(id=id)
    redis_client.flushall()
