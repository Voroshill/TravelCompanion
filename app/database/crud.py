from sqlalchemy.future import select

from app.database.models_db import Place


async def add_your_place(db_session, name: str, location: str, category: str):
    """
    Добавление уникальных место посредством ручного ввода
    Return: Возвращает вновь добавленное место
    """
    new_place = Place(name=name, location=location, category=category)
    db_session.add(new_place)
    await db_session.commit()
    return new_place


async def get_places(db_session):
    """
    Извлекает все места из базы данных.
    Return: Список объектов мест.
    """
    result = await db_session.execute(select(Place))
    return result.scalars().all()


async def add_place(db_session, name: str, location: str, category: str):
    """
    Автоматическое добавление нового места в базу данных, на основании выполненного к API запроса
    Param db_session: Сессия для работы с базой данных.
    Param name: Название места.
    Param location: Местоположение.
    Param category: Категория места.
    :return: Новый объект места с присвоенным id или None, если такое место уже существует.
    """
    existing_place = await db_session.execute(select(Place).filter_by(name=name, location=location, category=category))
    existing_place = existing_place.scalars().first()

    if existing_place:
        return None

    new_place = Place(name=name, location=location, category=category)
    db_session.add(new_place)
    await db_session.commit()
    return new_place
