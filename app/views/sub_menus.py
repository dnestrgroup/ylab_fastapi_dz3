import json
from typing import List
from app.db.base import get_db
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from app.db.redis.redis import redis_client
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositorie_for_submenu import RepositoriesSubMenus
from app.schemas.schemas import CreateSubMenuRequest, SubMenuResponse

router = APIRouter()


@router.get("/api/v1/menus/{id_menu}/submenus", response_model=List[SubMenuResponse])
async def get_menus(id_menu: int, db: AsyncSession = Depends(get_db)) -> List[SubMenuResponse]:
    cached_data = redis_client.get("/api/v1/menus/{id_menu}/submenus")
    if cached_data:
        list_menu = json.loads(cached_data)
        return [SubMenuResponse(**json.loads(submenu)) for submenu in list_menu]
    repo_sm = RepositoriesSubMenus(db)
    list_menu = await repo_sm.get_list_submenus(id_menu)
    submenus_for_redis = [submenu.json() for submenu in list_menu]
    redis_client.setex("/api/v1/menus/{id_menu}/submenus", 1000, json.dumps(submenus_for_redis))
    return list_menu


@router.get(
    "/api/v1/menus/{id_menu}/submenus/{id_submenu}", response_model=SubMenuResponse
)
async def get_submenu(
    id_menu: int, id_submenu: int, db: AsyncSession = Depends(get_db)
) -> SubMenuResponse:
    cached_data = redis_client.get("/api/v1/menus/" + str(id_menu) + "/submenus/" + str(id_submenu))
    if cached_data:
        return SubMenuResponse(**json.loads(cached_data))
    repo_sm = RepositoriesSubMenus(db)
    res = await repo_sm.get_submenu(id_menu, id_submenu)
    if res:
        redis_client.setex("/api/v1/menus/" + str(id_menu) + "/submenus/" + str(id_submenu), 1000, res.json())
        return res
    raise HTTPException(status_code=404, detail="submenu not found")


@router.patch(
    "/api/v1/menus/{id_menu}/submenus/{id_submenu}", response_model=SubMenuResponse
)
async def patch_submenu(
    id_menu: int, id_submenu: int, data: CreateSubMenuRequest, db: AsyncSession = Depends(get_db)
) -> SubMenuResponse:
    repo_sm = RepositoriesSubMenus(db)
    res = await repo_sm.patch_submenu(id_menu, id_submenu, data)
    redis_client.flushall()
    return res

@router.post(
    "/api/v1/menus/{id_menu}/submenus", response_model=SubMenuResponse, status_code=201
)
async def post_submenu(
    data: CreateSubMenuRequest, id_menu: int, db: AsyncSession = Depends(get_db)
) -> SubMenuResponse:
    repo_sm = RepositoriesSubMenus(db)
    res = await repo_sm.post_submenu(data, id_menu)
    redis_client.flushall()
    return res

@router.delete("/api/v1/menus/{id_menu}/submenus/{id_submenu}")
async def delete_submenu(id_submenu: int, db: AsyncSession = Depends(get_db)) -> None:
   repo_sm = RepositoriesSubMenus(db)
   redis_client.flushall()
   await repo_sm.delete_submenu(id_submenu=id_submenu)