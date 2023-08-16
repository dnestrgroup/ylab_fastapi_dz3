from fastapi import BackgroundTasks, Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.schemas import CreateMenuRequest, MenuResponse
from app.services.cache_invalidation import cache_invalidation
from app.services.service_menu import MenuService
from app.services.upload_menu import UploadMenu

router = APIRouter()


@router.get('/start')
async def start(db: AsyncSession = Depends(get_db)) -> str:
    """
    Ручка для удобства запуска обновления данных из xlsx (Для себя))))
    """
    upload_menu = UploadMenu(db=db)
    await upload_menu.run()
    return 'start'


@router.get('/api/v1/menus', response_model=list[MenuResponse], summary='Метод получения списка меню')
async def get_menus(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)) -> list[MenuResponse]:
    menu_service = MenuService(db=db)
    response = await menu_service.get_list()
    background_tasks.add_task(cache_invalidation, '/api/v1/menus')
    return response


@router.get('/api/v1/menus/{id}', response_model=MenuResponse)
async def get_menu(background_tasks: BackgroundTasks, id: int, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    menu_service = MenuService(db=db)
    response = await menu_service.get_one_menu_by_id(id=id)
    background_tasks.add_task(cache_invalidation, url='/api/v1/menus/' + str(id))
    return response


@router.patch('/api/v1/menus/{id}', response_model=CreateMenuRequest)
async def patch_menu(background_tasks: BackgroundTasks, id: int, data: CreateMenuRequest, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    menu_service = MenuService(db=db)
    background_tasks.add_task(cache_invalidation, url='/api/v1/menus/' + str(id))
    return await menu_service.update_menu(id=id, data=data)


@router.post('/api/v1/menus', response_model=MenuResponse, status_code=201)
async def post_menu(background_tasks: BackgroundTasks, data: CreateMenuRequest, db: AsyncSession = Depends(get_db)) -> MenuResponse:
async def post_menu(background_tasks: BackgroundTasks, data: CreateMenuRequest, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    menu_service = MenuService(db=db)
    response = await menu_service.create_menu(data=data)
    background_tasks.add_task(cache_invalidation, '/api/v1/menus')
    return response
    response = await menu_service.create_menu(data=data)
    background_tasks.add_task(cache_invalidation, '/api/v1/menus')
    return response


@router.delete('/api/v1/menus/{id}')
async def delete_menu(background_tasks: BackgroundTasks, id: int, db: AsyncSession = Depends(get_db)) -> None:
async def delete_menu(background_tasks: BackgroundTasks, id: int, db: AsyncSession = Depends(get_db)) -> None:
    menu_service = MenuService(db=db)
    response = await menu_service.delete_menu(id=id)
    background_tasks.add_task(cache_invalidation, '/api/v1/menus' + str(id))
    return response
    response = await menu_service.delete_menu(id=id)
    background_tasks.add_task(cache_invalidation, '/api/v1/menus' + str(id))
    return response


@router.get('/api/v1/restaraunt')
async def get_menus_all(db: AsyncSession = Depends(get_db)):
    menu_service = MenuService(db=db)
    return await menu_service.get_all()
