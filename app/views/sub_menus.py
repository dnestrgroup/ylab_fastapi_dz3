from fastapi import Depends, BackgroundTasks
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.schemas import CreateSubMenuRequest, SubMenuResponse
from app.services.cache_invalidation import cache_invalidation
from app.services.service_submenu import SubMenuService

router = APIRouter()


@router.get('/api/v1/menus/{id_menu}/submenus', response_model=list[SubMenuResponse])
async def get_submenus(id_menu: int, db: AsyncSession = Depends(get_db)) -> list[SubMenuResponse]:
    sbmenu_service = SubMenuService(db=db)
    return await sbmenu_service.get_list_submenus(id_menu=id_menu)


@router.get(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}', response_model=SubMenuResponse
)
async def get_submenu(
    id_menu: int, id_submenu: int, db: AsyncSession = Depends(get_db)
) -> SubMenuResponse:
    sbmenu_service = SubMenuService(db=db)
    return await sbmenu_service.get_one_submenu_by_id(id_menu, id_submenu)


@router.patch(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}', response_model=SubMenuResponse
)
async def patch_submenu(
    background_tasks: BackgroundTasks, id_menu: int, id_submenu: int, data: CreateSubMenuRequest, db: AsyncSession = Depends(get_db)
) -> SubMenuResponse:
    sbmenu_service = SubMenuService(db=db)
    response = await sbmenu_service.update_submenu(data, id_menu, id_submenu)
    background_tasks.add_task(cache_invalidation, '/api/v1/menus' + str(id_menu) + '/submenus' + str(id_submenu))
    return response


@router.post(
    '/api/v1/menus/{id_menu}/submenus', response_model=SubMenuResponse, status_code=201
)
async def post_submenu(
    background_tasks: BackgroundTasks, data: CreateSubMenuRequest, id_menu: int, db: AsyncSession = Depends(get_db)
) -> SubMenuResponse:
    sbmenu_service = SubMenuService(db=db)
    response = await sbmenu_service.create_submenu(data, id_menu)
    background_tasks.add_task(cache_invalidation, '/api/v1/menus' + str(id_menu) + '/submenus')
    return response


@router.delete('/api/v1/menus/{id_menu}/submenus/{id_submenu}')
async def delete(background_tasks: BackgroundTasks, id_menu: int, id_submenu: int, db: AsyncSession = Depends(get_db)) -> None:
    sbmenu_service = SubMenuService(db=db)
    response = await sbmenu_service.delete_submenu(id_menu, id_submenu)
    background_tasks.add_task(cache_invalidation, '/api/v1/menus' + str(id_menu) + '/submenus' + str(id_submenu))
    return response
