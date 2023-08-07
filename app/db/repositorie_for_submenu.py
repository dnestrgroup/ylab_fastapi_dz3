from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import Dishes, SubMenu
from app.schemas.schemas import CreateSubMenuRequest, SubMenuResponse


class RepositoriesSubMenus:
    def __init__(self, db: AsyncSession = None):
        self.db = db

    async def get_list_submenus(self, id: int):
        query = select(SubMenu).filter(SubMenu.main_menu_id == id)
        list_submenus = []
        for submenu in (await self.db.execute(query)).scalars():
            list_submenus.append(
                SubMenuResponse(
                    id=submenu.id,
                    title=submenu.title,
                    description=submenu.description
                )
            )
        return list_submenus

    async def get_submenu(self, id_menu: int, id_submenu: int):
        query = select(SubMenu).filter(SubMenu.id == id_submenu)
        res = (await self.db.execute(query)).scalar_one_or_none()
        if res is not None:
            dishes_query = select(func.count(Dishes.id)).where(
                Dishes.sub_menu_id == id_submenu
            )
            dishes_count = (await self.db.execute(dishes_query)).scalar()
            return SubMenuResponse(
                id=res.id,
                title=res.title,
                description=res.description,
                dishes_count=dishes_count,
            )

    async def patch_submenu(self, id_menu: int, id_submenu: int, data: CreateSubMenuRequest):
        query = (
            update(SubMenu)
            .where(SubMenu.id == id_submenu)
            .values(title=data.title, description=data.description)
            .returning(SubMenu.id, SubMenu.title, SubMenu.description)
        )
        res = (await self.db.execute(query)).fetchone()
        await self.db.commit()
        return SubMenuResponse(id=res[0], title=res[1], description=res[2])

    async def post_submenu(self, data: CreateSubMenuRequest, id_menu: int):
        query = (
            insert(SubMenu)
            .values(title=data.title, description=data.description, main_menu_id=id_menu)
            .returning(SubMenu.id, SubMenu.title, SubMenu.description)
        )
        result = (await self.db.execute(query)).fetchone()
        await self.db.commit()
        return SubMenuResponse(
            id=result[0], title=result[1], description=result[2], dishes_count=None
        )

    async def delete_submenu(self, id_submenu: int):
        query = delete(SubMenu).where(SubMenu.id == id_submenu)
        await self.db.execute(query)
        await self.db.commit()
