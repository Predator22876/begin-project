import asyncio
import time


async def login():
    print("Авторизуем пользователя...")
    await asyncio.sleep(1)
    print("Пользователь авторизован")
    return 42


async def get_user_profile(user_id):
    print(f"Получаем профиль пользователя {user_id}...")
    await asyncio.sleep(1)
    print("Профиль получен")
    return {"user_id": user_id, "name": "Алексей"}


async def get_user_bookings(user_id):
    print(f"Получаем бронирования пользователя {user_id}...")
    await asyncio.sleep(2)
    print("Бронирования получены")
    return [
        {"hotel": "AZIMUT Сити Отель Смоленская", "city": "Москва"},
        {"hotel": "Cosmos Saint-Petersburg Nevsky Hotel", "city": "Санкт-Петербург"}
    ]


async def get_popular_hotels():
    print("Получаем список популярных отелей...")
    await asyncio.sleep(3)
    print("Популярные отели получены")
    return [
        {"hotel": "Marins Park Hotel", "city": "Сочи"},
        {"hotel": "AZIMUT Отель", "city": "Казань"},
        {"hotel": "Cosmos Selection", "city": "Москва"}
    ]


async def get_recommendations(bookings):
    print("Получаем персональные рекомендации...")
    await asyncio.sleep(1)
    print("Рекомендации получены")
    return [
        {"hotel": "Гранд Отель Жемчужина", "city": "Сочи"},
        {"hotel": "AZIMUT Парк Отель", "city": "Переславль-Залесский"}
    ]


async def build_dashboard(profile, bookings, popular_hotels, recommendations):
    print("Собираем дашборд...")
    await asyncio.sleep(0.2)
    return {
        "profile": profile,
        "bookings": bookings,
        "popular_hotels": popular_hotels,
        "recommendations": recommendations
    }


async def main():
    start_time = time.perf_counter()

    user_id = await login()
    profile, bookings, popular_hotels = await asyncio.gather(
        get_user_profile(user_id),
        get_user_bookings(user_id),
        get_popular_hotels()
    )
    
    recommendations = await get_recommendations(bookings)

    dashboard = await build_dashboard(
        profile,
        bookings,
        popular_hotels,
        recommendations
    )

    print("Времени прошло:", time.perf_counter() - start_time)


if __name__ == "__main__":
    asyncio.run(main())