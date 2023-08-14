from typing import Any, Dict

import pandas as pd
from sqlalchemy import delete, not_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import Dishes, MainMenu, SubMenu


class UploadMenu():
    def __init__(self, db: AsyncSession)->None:
        self.db=db

    async def run(self)->None:
        df = pd.read_excel('app/admin/Menu.xlsx', engine='openpyxl')
        data = df.values.tolist()
        set_of_menus:set = set()
        set_of_submenus:set = set()
        set_of_dishes:set = set()
        for i in data:
            # Если выбранная Excel-строка относится к Меню, то обрабатываем её здесь:
            if ((not str(i[1]).isdigit()) and (str(i[1])!='nan')):
                test_data:dict[str, Any]={'title':i[1],'description':i[2]}
                query = insert(MainMenu).values(**test_data).on_conflict_do_update(
                    constraint='uq_main_menu_title',
                    set_=test_data).returning(MainMenu.id)
                main_menu_id = (await self.db.execute(query)).scalar()
                await self.db.commit()
                set_of_menus.add(str(i[1]))

            # Если выбранная Excel-строка относится к Подменю, то обрабатываем её здесь:
            if (((str(i[1]).isdigit()) or (str(i[1])=='nan')) and ((not str(i[2]).isdigit()) and (str(i[2])!='nan'))):
                test_data={'title':i[2],'description':i[3], 'main_menu_id':main_menu_id}
                query = insert(SubMenu).values(**test_data).on_conflict_do_update(
                    constraint='uq_sub_menu_title',
                    set_=test_data).returning(SubMenu.id)
                sub_menu_id = (await self.db.execute(query)).scalar()
                await self.db.commit()
                set_of_submenus.add(str(i[2]))

            # Если выбранная Excel-строка относится к Блюдам, то обрабатываем её здесь:
            if (((str(i[1]).isdigit()) or (str(i[1])=='nan')) and (str(i[2]).isdigit()) or (str(i[2])=='nan') and ((not str(i[3]).isdigit()) and (i[3]!='nan'))):
                test_data = {'title': i[3], 'description': i[4], 'price': i[5], 'sub_menu_id': sub_menu_id}
                query = insert(Dishes).values(**test_data).on_conflict_do_update(
                    constraint='uq_dishes_title',
                    set_=test_data).returning(Dishes.id)
                dishes_id = (await self.db.execute(query)).scalar()
                await self.db.commit()
                set_of_dishes.add(str(i[3]))

        await self.db.execute(delete(MainMenu).where(not_(MainMenu.title.in_(set_of_menus))))
        await self.db.commit()
        await self.db.execute(delete(SubMenu).where(not_(SubMenu.title.in_(set_of_submenus))))
        await self.db.commit()
        await self.db.execute(delete(Dishes).where(not_(Dishes.title.in_(set_of_dishes))))
        await self.db.commit()
