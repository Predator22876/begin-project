# Запуск и обновление приложения на сервере

Инструкция рассчитана на Linux-сервер с установленными Docker Engine и Docker Compose
(команда `docker compose`). PostgreSQL и Redis работают в Docker-сети `myNetwork`;
API-контейнер при старте автоматически применяет миграции Alembic.

## 1. Подготовить сервер и постоянные контейнеры

Этот раздел нужен только при первом развёртывании, если PostgreSQL и Redis ещё не
запущены. Если контейнеры и сеть уже существуют, переходите к разделу 2.

Создайте Docker-сеть:

```bash
docker network create myNetwork
```

Создайте постоянный volume для базы и запустите PostgreSQL. Замените значения
`<...>` на собственные; пароль должен совпадать с `DB_PASS` в `.env` приложения.
Не используйте пароль из примеров или репозитория:

```bash
docker volume create pg-booking-data

docker run -d \
  --name booking_db \
  --restart unless-stopped \
  --network myNetwork \
  -e POSTGRES_USER=<пользователь_базы> \
  -e POSTGRES_PASSWORD=<надёжный_пароль> \
  -e POSTGRES_DB=<имя_базы> \
  -v pg-booking-data:/var/lib/postgresql/data \
  postgres:16-alpine
```

Запустите Redis в той же сети:

```bash
docker run -d \
  --name booking_cache \
  --restart unless-stopped \
  --network myNetwork \
  redis
```

Для подключения приложения не нужно публиковать PostgreSQL и Redis на публичные
порты сервера. Если контейнеры уже созданы, убедитесь, что они подключены к сети:

```bash
docker network connect myNetwork booking_db
docker network connect myNetwork booking_cache
```

Если команда сообщает, что контейнер уже подключён к сети, это нормально.

## 2. Настроить приложение

В каталоге проекта на сервере создайте или отредактируйте `.env`. Файл должен
содержать все обязательные настройки из `src/config.py`. Как минимум проверьте,
что адреса БД и Redis — это имена контейнеров, а порт PostgreSQL внутри Docker-сети
обычно `5432`:

```dotenv
MODE=PROD
DB_NAME=<имя_базы>
DB_HOST=booking_db
DB_PORT=5432
DB_USER=<пользователь_базы>
DB_PASS=<надёжный_пароль>
REDIS_HOST=booking_cache
REDIS_PORT=6379
JWT_SECRET_KEY=<длинный_случайный_секрет>
JWT_ALGORITHM=<алгоритм_из_вашей_конфигурации>
ACCESS_TOKEN_EXPIRE_MINUTES=<время_действия_токена_в_минутах>
```

`DB_NAME`, `DB_USER` и `DB_PASS` должны соответствовать параметрам PostgreSQL.
Оставьте настройки JWT и остальные уже используемые значения проекта корректными.
Не добавляйте `.env` в Git и не публикуйте его содержимое.

## 3. Обновить код и запустить Compose

Перейдите в каталог проекта, получите версию кода с исправлением и проверьте, что
рядом находятся `Dockerfile`, `docker-compose.yml` и `.env`. Например, если проект
уже клонирован и нужные изменения отправлены в текущую ветку:

```bash
git pull
```

Соберите образы и запустите сервисы:

```bash
docker compose up --build -d
```

При старте контейнер `booking_back` выполняет `alembic upgrade head` до запуска API.
Новая миграция добавляет уникальное ограничение на `hotels.location`. Пока миграция
не завершилась успешно, API не запустится.

Проверьте состояние контейнеров и логи API:

```bash
docker compose ps
docker compose logs --tail=200 booking_back
```

Если миграция применилась, в логах не должно быть ошибки Alembic, а API должен
запуститься. При ошибке миграции сначала устраните указанную в логах причину, затем
повторите запуск:

```bash
docker compose up --build -d
```

## 4. Проверить доступность приложения

Compose запускает API на порту `8000` внутри Docker-сети, но сам порт наружу не
публикует. В текущей конфигурации для доступа снаружи используется Nginx, который
направляет запросы на `booking_back:8000`. Если Nginx ещё не запущен, из каталога
проекта выполните:

```bash
docker run -d \
  --name booking_nginx \
  --restart unless-stopped \
  --network myNetwork \
  -p 80:80 \
  -v "$PWD/nginx.conf:/etc/nginx/nginx.conf:ro" \
  nginx
```

Откройте `http://<адрес-сервера>/docs`. Для публичного production-сервера настройте
HTTPS и ограничьте доступ к серверным портам средствами firewall.

Чтобы посмотреть логи или остановить сервисы приложения:

```bash
docker compose logs -f booking_back
docker compose down
```

`docker compose down` останавливает и удаляет контейнеры Compose, но не удаляет
volume PostgreSQL и не останавливает запущенные отдельно `booking_db`,
`booking_cache` и `booking_nginx`.

## Если миграция не применяет уникальность

В существующей базе могут уже быть отели с одинаковой локацией. В таком случае
PostgreSQL не сможет создать уникальное ограничение, и контейнер API завершится с
ошибкой. Проверьте дубликаты запросом:

```bash
docker exec -it booking_db sh -c \
  'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT location, COUNT(*) FROM hotels GROUP BY location HAVING COUNT(*) > 1;"'
```

Сначала вручную решите, какие данные сохранить или исправить, учитывая связанные с
отелями номера и бронирования. Не удаляйте записи автоматически: миграция намеренно
не выбирает за вас, какой отель оставить. После устранения дубликатов перезапустите
Compose:

```bash
docker compose up --build -d
docker compose logs --tail=200 booking_back
```

После успешного применения ограничения при создании отеля с уже занятой локацией
API вернёт HTTP `409 Conflict` с сообщением о существующей локации.
