from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.schemas import CreateDishesRequest, DishesResponse
from app.services.service_dishes import DishesService

router = APIRouter()


@router.get(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes',
    response_model=list[DishesResponse],
)
async def get_dishes(id_menu: int, id_submenu: int, db: AsyncSession = Depends(get_db)) -> list[DishesResponse]:
    ds_service = DishesService(db=db)
    return await ds_service.get_list_dishes(id_menu=id_menu, id_submenu=id_submenu)


@router.get(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{id_dishes}',
    response_model=DishesResponse,
)
async def get_dishes_one(
    id_menu: int, id_submenu: int, id_dishes: int, db: AsyncSession = Depends(get_db)
) -> DishesResponse:
    ds_service = DishesService(db=db)
    return await ds_service.get_one_dish_by_id(id_menu, id_submenu, id_dishes)


@router.patch(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{id_dishes}',
    response_model=DishesResponse
)
async def patch_dish(
    id_menu: int,
    id_submenu: int,
    id_dishes: int,
    data: CreateDishesRequest,
    db: AsyncSession = Depends(get_db),
) -> DishesResponse:
    ds_service = DishesService(db=db)
    return await ds_service.update_dish(id_menu, id_submenu, id_dishes, data)


@router.post(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes',
    response_model=DishesResponse,
    status_code=201,
)
async def post_dish(
    data: CreateDishesRequest,
    id_menu: int,
    id_submenu: int,
    db: AsyncSession = Depends(get_db)
) -> DishesResponse:
    ds_service = DishesService(db=db)
    return await ds_service.create_dish(data, id_menu, id_submenu)


@router.delete(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{id_dishes}',
)
async def delete_dishes(id_menu: int, id_submenu: int, id_dishes: int, db: AsyncSession = Depends(get_db)) -> None:
    ds_service = DishesService(db=db)
    await ds_service.delete_dish(id_menu, id_submenu, id_dishes)
