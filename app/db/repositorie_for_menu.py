from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.models import Dishes, MainMenu, SubMenu
from sqlalchemy import delete, func, insert, select, update
from app.schemas.schemas import CreateMenuRequest, MenuResponse

class RepositoriesMenus:
    def __init__(self, db: AsyncSession = None):
        self.db = db

    async def create(self, data: CreateMenuRequest):
        query = insert(MainMenu).values(**data.dict()).returning(MainMenu)
        result = (await self.db.execute(query)).scalar_one_or_none()
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def update(self, id: int, data: CreateMenuRequest):
        query = (
            update(MainMenu)
            .where(MainMenu.id == id)
            .values(**data.dict())
            .returning(MainMenu)
        )
        result = (await self.db.execute(query)).scalar_one_or_none()
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def delete(self, id: int):
        query = delete(MainMenu).where(MainMenu.id == id)
        await self.db.execute(query)
        await self.db.commit()

    async def get(self, id: int):
        query = select(MainMenu).filter(MainMenu.id == id)
        res = (await self.db.execute(query)).scalar_one_or_none()
        if res is None:
            return None
        submenus_query = select(func.count(SubMenu.id)).where(
            SubMenu.main_menu_id == id
        )
        submenus_count = (await self.db.execute(submenus_query)).scalar()
        submenus = select(SubMenu.id).where(SubMenu.main_menu_id == id)
        submenus_results = await self.db.execute(submenus)
        submenu_ids = [result[0] for result in submenus_results]
        dishes_query = select(func.count(Dishes.id)).where(
            Dishes.sub_menu_id.in_(submenu_ids)
        )
        dishes_count = (await self.db.execute(dishes_query)).scalar()
        return MenuResponse(
            id=res.id,
            title=res.title,
            description=res.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count,
        )

    async def get_list(self):
        query = select(MainMenu)
        list_menu = []
        for menu in (await self.db.execute(query)).scalars():
            list_menu.append(
                MenuResponse(
                    id=menu.id,
                    title=menu.title,
                    description=menu.description,
                )
            )
        return list_menu