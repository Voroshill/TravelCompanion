from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.places.static_filtration import Category
from app.places.crud import add_your_place, get_places, add_place
from app.db.session import init_db, get_db
from app.places.services import places_from_api, returning_places


router = APIRouter(
    prefix="/places",
    tags=["Поиск мест"],
)


@router.post("/search/", response_class=JSONResponse)
async def search_places(location: str, category: str):
    """
    Обработчик для получения списка мест по API Google по ключевому слову или фразе.
    Return: Список всех мест.
    """
    result = await places_from_api(location, category)
    places = returning_places(result)
    return JSONResponse(content={"places": places})


@router.post('/searchwithfilter/', response_class=JSONResponse)
async def search_places_withfilters(location: str, category: Category):
    """
    Обработчик для получения списка мест по API Google по статичным категориям
    из модели Category(app/static_filtration.py).
    Return: Список всех мест соответствующих категории.
    """
    result = await places_from_api(location, category)
    places_filtered = returning_places(result, category)
    return JSONResponse(content={"places": places_filtered})


@router.get("/categories/")
async def get_categories():
    """
    Эндпоинт для получения всех доступных категорий.
    """
    categories = [category.value for category in Category]
    return JSONResponse(content={"categories": categories})


@router.on_event("startup")
async def startup():
    await init_db()


@router.post("/add_place/")
async def create_place(name: str, location: str, category: str, db: AsyncSession = Depends(get_db)):
    """
    Обработчик для добавления нового места в базу данных.
    Name: Название места.
    Location: Местоположение.
    Category: Категория места.
    Возвращает: Информация о добавленном месте (id и название).
    """
    new_place = await add_your_place(db, name, location, category)
    return {"id": new_place.id, "name": new_place.name}


@router.get("/db_places/")
async def read_places_from_db(db: AsyncSession = Depends(get_db)):
    """
    Обработчик для получения списка всех мест из базы данных.
    Возвращает: Список всех мест.
    """
    places = await get_places(db)
    return places


@router.post('/search_and_save/')
async def search_and_save(location: str, category: str, db: AsyncSession = Depends(get_db)):
    """
    Обработчик для поиска мест через API Google и их сохранения в базе данных.
    Сохраняет только уникальные места, которые не были найдены в предыдущих запросах.

    Location: Местоположение для поиска (например, город).
    Category: Категория мест (например, ресторан, кафе).
    Возвращает: Список сохраненных уникальных мест.
    """
    result = await places_from_api(location, category)

    if isinstance(result, dict) and 'detail' in result:
        return result

    saved_places = []
    for place in result:
        name = place['name']
        location = place['formatted_address']

        saved_place = await add_place(db, name, location, category)
        if saved_place:
            saved_places.append({
                "name": saved_place.name,
                "location": saved_place.location,
                "category": saved_place.category
            })

    return {"saved_places": saved_places}
