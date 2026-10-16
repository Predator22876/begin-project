
# 🚀 Запуск приложения

## Первый запуск: поднять БД и кэш (один раз)

Выполните эти команды только один раз. Данные в БД и кэше будут сохранены между перезапусками приложения.

### Для Bash/Linux/Mac:

```bash
# Создать сеть Docker
docker network create myNetwork

# Поднять PostgreSQL
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=sdklafjlkasdjflksdfsdl \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16-alpine

# Поднять Redis
docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis

#Поднять Nginx
docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=myNetwork \ 
    --d 80:80 nginx
```
### Для PowerShell (Windows):

```powershell
# Создать сеть Docker
docker network create myNetwork

# Поднять PostgreSQL
docker run --name booking_db -p 6432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=sdklafjlkasdjflksdfsdl -e POSTGRES_DB=booking --network=myNetwork --volume pg-booking-data:/var/lib/postgresql/data -d postgres:16-alpine

# Поднять Redis
docker run --name booking_cache -p 7379:6379 --network=myNetwork -d redis
```

## Запуск приложения (многократно)

После первого запуска БД и кэша, используйте Docker Compose для запуска приложения:

```bash
# Собрать и запустить все контейнеры (API + Celery)
docker compose up --build

# Или запустить в фоне (-d флаг)
docker compose up --build -d

# Посмотреть логи
docker compose logs -f booking_back

# Остановить приложение (БД и кэш останутся живы)
docker compose down
```

## 📖 Доступ к приложению

- **FastAPI Документация (Swagger)**: http://localhost:8000/docs
- **PostgreSQL**: `localhost:6432` (пользователь: postgres, пароль: postgres)
- **Redis**: `localhost:7379`

## Очистка всего (если нужно начать заново)

### Для Bash/Linux/Mac:

```bash
# Остановить и удалить все контейнеры и сеть
docker compose down -v
docker rm -f booking_db booking_cache 2>/dev/null
docker network rm myNetwork 2>/dev/null

# Потом повторить первый и второй пункты выше
```

### Для PowerShell (Windows):

```powershell
# Остановить и удалить все контейнеры и сеть
docker compose down -v
docker rm -f booking_db booking_cache
docker network rm myNetwork

# Потом повторить первый и второй пункты выше
```  