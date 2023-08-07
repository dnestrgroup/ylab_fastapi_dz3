from app.db.models.models import Dishes
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select, update
from app.schemas.schemas import CreateDishesRequest, DishesResponse

class RepositoriesDishes:
    def __init__(self, db: AsyncSession = None):
        self.db = db
    
    async def get_list_dishes(self, id: int):
        query = select(Dishes).filter(Dishes.sub_menu_id == id)
        list_dishes = []
        for dishes in (await self.db.execute(query)).scalars():
            list_dishes.append(
                DishesResponse(
                    id=dishes.id,
                    title=dishes.title,
                    description=dishes.description,
                    price=dishes.price,
                )
            )
        return list_dishes
    
    async def get_dish_one_by_id(self, id_menu: int, id_submenu: int, id_dishes: int):
        query = select(Dishes).filter(Dishes.id == id_dishes)
        res = (await self.db.execute(query)).scalar_one_or_none()
        if res is not None:
            return DishesResponse(id=str(res.id), title=res.title, description=res.description, price=str(res.price))

    async def patch_dish(self, id_menu: int, id_submenu: int, id_dishes: int, data: CreateDishesRequest):
        query = (
            update(Dishes)
            .where(Dishes.id == id_dishes)
            .values(title=data.title, description=data.description, price=data.price)
            .returning(Dishes.id, Dishes.title, Dishes.description, Dishes.price)
        )
        res = (await self.db.execute(query)).fetchone()
        await self.db.commit()
        return DishesResponse(id=res[0], title=res[1], description=res[2], price=res[3])
    
    async def post_dish_new(self, data: CreateDishesRequest, id_menu: int, id_sub_menu: int):
        query = (
            insert(Dishes)
            .values(
                title=data.title,
                description=data.description,
                sub_menu_id=id_sub_menu,
                price=data.price,
            )
            .returning(Dishes.id, Dishes.title, Dishes.description, Dishes.price)
        )
        result = (await self.db.execute(query)).fetchone()
        await self.db.commit()
        if result:
            return DishesResponse(id=str(result[0]), title=result[1], description=result[2], price=result[3])
    
    async def delete_dish_by_id(self, id_menu: int, id_submenu: int, id_dishes: int):
        query = (
            delete(Dishes)
            .where(Dishes.id == id_dishes)
        )
        res = await self.db.execute(query)
        await self.db.commit()
