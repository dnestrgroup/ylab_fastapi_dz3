import json

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.redis.redis import redis_client
from app.db.repositorie_for_dish import RepositoriesDishes
from app.schemas.schemas import CreateDishesRequest, DishesResponse

router = APIRouter()


@router.get(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes',
    response_model=list[DishesResponse],
)
async def get_dishes(id_menu: int, id_submenu: int, db: AsyncSession = Depends(get_db)) -> list[DishesResponse]:
    cached_data = redis_client.get(
        f'/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes')
    if cached_data:
        list_dishes = json.loads(cached_data)
        return [DishesResponse(**json.loads(dish)) for dish in list_dishes]
    repo_d = RepositoriesDishes(db)
    list_dishes = await repo_d.get_list(id_submenu)
    dishes_for_redis = [dish.json() for dish in list_dishes]
    redis_client.setex(
        '/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes', 1000, json.dumps(dishes_for_redis))
    return list_dishes


@router.get(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{id_dishes}',
    response_model=DishesResponse,
)
async def get_dishes_one(
    id_menu: int, id_submenu: int, id_dishes: int, db: AsyncSession = Depends(get_db)
) -> DishesResponse:
    cached_data = redis_client.get(
        '/api/v1/menus/' + str(id_menu) + '/submenus/' + str(id_submenu) + '/dishes/' + str(id_dishes))
    if cached_data:
        return DishesResponse(**json.loads(cached_data))
    repo_d = RepositoriesDishes(db)
    res = await repo_d.get(id_menu, id_submenu, id_dishes)
    if res:
        redis_client.setex(
            f'/api/v1/menus/{str(id_menu)}/submenus/{str(id_submenu)}/dishes/{ str(id_dishes)}', 1000, res.json())
        return res
    raise HTTPException(status_code=404, detail='dish not found')


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
    repo_d = RepositoriesDishes(db)
    res = await repo_d.update(id_menu, id_submenu, id_dishes, data)
    # redis_client.flushall()
    response_dish = DishesResponse(
        id=res.id,
        title=res.title,
        description=res.description,
        price=res.price
    )
    redis_client.setex(
        f'/api/v1/menus/{str(id_menu)}/submenus/{str(id_submenu)}/dishes/{str(id_dishes)}', 1000, response_dish.json())
    return res


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
    repo_d = RepositoriesDishes(db)
    res = await repo_d.create(data, id_menu, id_submenu)
    if res:
        redis_client.delete(f'/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes')
        redis_client.setex(f'/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{res.id}', 1000, res.json())
    return res


@router.delete(
    '/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{id_dishes}',
)
async def delete_dishes(id_menu: int, id_submenu: int, id_dishes: int, db: AsyncSession = Depends(get_db)) -> None:
    repo_d = RepositoriesDishes(db)
    redis_client.delete(f'/api/v1/menus/{str(id_menu)}/submenus/{str(id_submenu)}/dishes/{str(id_dishes)}')
    redis_client.delete(f'/api/v1/menus/{str(id_menu)}/submenus/{str(id_submenu)}')
    await repo_d.delete(id_dishes=id_dishes)
