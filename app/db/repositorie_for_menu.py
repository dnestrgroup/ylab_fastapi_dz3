from sqlalchemy import delete, func, insert, join, select, update
from sqlalchemy import delete, func, insert, join, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.orm import aliased

from app.db.models.models import Dishes, MainMenu, SubMenu
from app.schemas.schemas import (
    CreateMenuRequest,
    MenuResponse,
)


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

    async def get_all(self):
        main_menu_alias = aliased(MainMenu)
        sub_menu_alias = aliased(SubMenu)
        dishes_alias = aliased(Dishes)
        sub_menu_alias_2 = aliased(SubMenu)

        query = select(main_menu_alias, sub_menu_alias, dishes_alias).select_from(
            join(main_menu_alias, sub_menu_alias, main_menu_alias.id == sub_menu_alias.main_menu_id)
        ).select_from(
            join(sub_menu_alias_2, dishes_alias, sub_menu_alias_2.id == dishes_alias.sub_menu_id)
        ).where(
            sub_menu_alias.main_menu_id == main_menu_alias.id,
            dishes_alias.sub_menu_id == sub_menu_alias_2.id
        )
        result = (await self.db.execute(query)).all()
        dict_menus = []

        for menu, sub_menu, dishes in result:
            menu_title = menu.title
            sub_menu_title = sub_menu.title

            dish_dict = {
                'Title': dishes.title,
                'Description': dishes.description,
                'Price': str(dishes.price),
            }
            menu_found = False
            for menu_dict in dict_menus:
                if menu_title in menu_dict:
                    menu_found = True
                    sub_menu_found = False
                    for sub_menu_dict in menu_dict[menu_title]:
                        if sub_menu_title in sub_menu_dict:
                            sub_menu_found = True
                            if dishes.sub_menu_id == sub_menu.id and menu.id == sub_menu.main_menu_id:
                                sub_menu_dict[sub_menu_title].append(dish_dict)
                            break
                    if not sub_menu_found:
                        if dishes.sub_menu_id == sub_menu.id and menu.id == sub_menu.main_menu_id:
                            sub_menu_dict = {sub_menu_title: []} if not sub_menu_found else sub_menu_dict
                            sub_menu_dict[sub_menu_title].append(dish_dict)
                            menu_dict[menu_title].append(sub_menu_dict)
                    break
            if not menu_found:
                if dishes.sub_menu_id == sub_menu.id and menu.id == sub_menu.main_menu_id:
                    dict_menus.append({menu_title: [{sub_menu_title: [dish_dict]}]})

        return dict_menus

    async def get_all(self):
        main_menu_alias = aliased(MainMenu)
        sub_menu_alias = aliased(SubMenu)
        dishes_alias = aliased(Dishes)
        sub_menu_alias_2 = aliased(SubMenu)

        query = select(main_menu_alias, sub_menu_alias, dishes_alias).select_from(
            join(main_menu_alias, sub_menu_alias, main_menu_alias.id == sub_menu_alias.main_menu_id)
        ).select_from(
            join(sub_menu_alias_2, dishes_alias, sub_menu_alias_2.id == dishes_alias.sub_menu_id)
        ).where(
            sub_menu_alias.main_menu_id == main_menu_alias.id,
            dishes_alias.sub_menu_id == sub_menu_alias_2.id
        )
        result = (await self.db.execute(query)).all()
        dict_menus = []

        for menu, sub_menu, dishes in result:
            menu_title = menu.title
            sub_menu_title = sub_menu.title

            dish_dict = {
                'Title': dishes.title,
                'Description': dishes.description,
                'Price': str(dishes.price),
            }
            menu_found = False
            for menu_dict in dict_menus:
                if menu_title in menu_dict:
                    menu_found = True
                    sub_menu_found = False
                    for sub_menu_dict in menu_dict[menu_title]:
                        if sub_menu_title in sub_menu_dict:
                            sub_menu_found = True
                            if dishes.sub_menu_id == sub_menu.id and menu.id == sub_menu.main_menu_id:
                                sub_menu_dict[sub_menu_title].append(dish_dict)
                            break
                    if not sub_menu_found:
                        if dishes.sub_menu_id == sub_menu.id and menu.id == sub_menu.main_menu_id:
                            sub_menu_dict = {sub_menu_title: []} if not sub_menu_found else sub_menu_dict
                            sub_menu_dict[sub_menu_title].append(dish_dict)
                            menu_dict[menu_title].append(sub_menu_dict)
                    break
            if not menu_found:
                if dishes.sub_menu_id == sub_menu.id and menu.id == sub_menu.main_menu_id:
                    dict_menus.append({menu_title: [{sub_menu_title: [dish_dict]}]})

        return dict_menus
