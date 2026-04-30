

docker network create myNetwork

docker run --name booking_db 
    -p 6432:5432 
    -e POSTGRES_USER=postgres 
    -e POSTGRES_PASSWORD=postgres 
    -e POSTGRES_DB=booking 
    --network=myNetwork 
    --volume pg-booking-data:/var/lib/postgresql/data 
    -d postgres

docker run --name booking_cache 
    -p 7379:6379
    --network=myNetwork 
    -d redis

docker run --name booking_back
    -p 8000:8000
    --network=myNetwork 
    booking_image

docker run --name booking_celery_worker
    --network=myNetwork 
    booking_image
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat
    --network=myNetwork 
    booking_image
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker build -t booking_image .  