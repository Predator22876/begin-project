import asyncio
from time import sleep
import os
from PIL import Image

from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager
from src.database import async_session_maker


@celery_instance.task
def test_task():
    sleep(5)
    print("PENIS")
    
@celery_instance.task
def resize_image(image_path: str, quality=85):
    # Проверяем, существует ли исходный файл
    sizes = [200, 500, 1000, 10000]
    output_dir="src/static/images"

    # Открываем изображение
    with Image.open(image_path) as img:
        original_format = img.format
        # Получаем базовое имя файла и расширение
        base_name, ext = os.path.splitext(os.path.basename(image_path))
        # Приводим расширение к нижнему регистру для сравнения
        ext = ext.lower()

        for target_size in sizes:
            # Создаём копию, чтобы не менять оригинал
            img_copy = img.copy()
            # Изменяем размер: максимальная сторона станет <= target_size, пропорции сохраняются
            img_copy.thumbnail((target_size, target_size), Image.LANCZOS)

            # Формируем имя выходного файла
            output_filename = f"{base_name}_{target_size}{ext}"
            output_path = os.path.join(output_dir, output_filename)

            # Сохраняем с оптимальными настройками в зависимости от формата
            if original_format == 'JPEG' or ext in ('.jpg', '.jpeg'):
                img_copy.save(output_path, 'JPEG', quality=quality, optimize=True)
            elif original_format == 'PNG' or ext == '.png':
                img_copy.save(output_path, 'PNG', optimize=True)
            else:
                # Для остальных форматов сохраняем как есть
                img_copy.save(output_path)

            print(f"Сохранено: {output_path} (размер: {img_copy.size})")

    print("Готово!")

async def get_bookings_with_today_checkin_helper():
    print("ФУНКЦИЯ НАЧАЛАСЬ")
    async with DBManager(session_factory=async_session_maker) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings}")

@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
