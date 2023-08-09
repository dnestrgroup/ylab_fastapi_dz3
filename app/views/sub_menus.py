import json

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.redis.redis import redis_client
from app.db.repositorie_for_submenu import RepositoriesSubMenus
from app.schemas.schemas import CreateSubMenuRequest, SubMenuResponse

router = APIRouter()


@router.get('/api/v1/menus/{id_menu}/submenus', response_model=list[SubMenuResponse])
async def get_submenus(id_menu: int, db: AsyncSession = Depends(get_db)) -> list[SubMenuResponse]:
    cached_data = redis_client.get(f'/api/v1/menus/{id_menu}/submenus')
    if cached_data:
        list_menu = json.loads(cached_data)
        return [SubMenuResponse(**json.loads(submenu)) for submenu in list_menu]
    repo_sm = RepositoriesSubMenus(db)
    list_menu = await repo_sm.get_list(id_menu)
    submenus_for_redis = [submenu.json() for submenu in list_menu]
    redis_client.setex(
        '/api/v1/menus/{id_menu}/submenus', 1000, json.dumps(submenus_for_redis))
    return list_menu


@router.get(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}', response_model=SubMenuResponse
)
async def get_submenu(
    id_menu: int, id_submenu: int, db: AsyncSession = Depends(get_db)
) -> SubMenuResponse:
    cached_data = redis_client.get(
        '/api/v1/menus/' + str(id_menu) + '/submenus/' + str(id_submenu))
    if cached_data:
        return SubMenuResponse(**json.loads(cached_data))
    repo_sm = RepositoriesSubMenus(db)
    res = await repo_sm.get(id_menu, id_submenu)
    if res:
        redis_client.setex('/api/v1/menus/' + str(id_menu) + '/submenus/' + str(id_submenu), 1000, res.json())
        return res
    raise HTTPException(status_code=404, detail='submenu not found')


@router.patch(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}', response_model=SubMenuResponse
)
async def patch_submenu(
    id_menu: int, id_submenu: int, data: CreateSubMenuRequest, db: AsyncSession = Depends(get_db)
) -> SubMenuResponse:
    repo_sm = RepositoriesSubMenus(db)
    res = await repo_sm.update(id_menu, id_submenu, data)
    response_sm = SubMenuResponse(
        id=res.id,
        title=res.title,
        description=res.description,
        dishes_count=0)
    redis_client.setex(f'/api/v1/menus/{str(id_menu)}/submenus/{str(id_submenu)}', 1000, response_sm.json())
    return res


@router.post(
    '/api/v1/menus/{id_menu}/submenus', response_model=SubMenuResponse, status_code=201
)
async def post_submenu(
    data: CreateSubMenuRequest, id_menu: int, db: AsyncSession = Depends(get_db)
) -> SubMenuResponse:
    repo_sm = RepositoriesSubMenus(db)
    res = await repo_sm.create(data, id_menu)
    if res:
        redis_client.delete(f'/api/v1/menus/{id_menu}/submenus')
        res.dishes_count = 0
        redis_client.setex(f'/api/v1/menus/{id_menu}/submenus/{res.id}', 1000, res.json())
    return res


@router.delete('/api/v1/menus/{id_menu}/submenus/{id_submenu}')
async def delete(id_menu: int, id_submenu: int, db: AsyncSession = Depends(get_db)) -> None:
    repo_sm = RepositoriesSubMenus(db)
    redis_client.delete(f'/api/v1/menus/{str(id_menu)}/submenus/{str(id_submenu)}')
    redis_client.delete(f'/api/v1/menus/{str(id_menu)}')
    await repo_sm.delete(id_submenu=id_submenu)
