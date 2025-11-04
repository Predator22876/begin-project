from fastapi import FastAPI
import uvicorn

import sys
import os

# Добавляем корень проекта в sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.api.hotels import router as router_hotels

app = FastAPI()

app.include_router(router_hotels)

if __name__ == "__main__":
    uvicorn.run("main:app", reload= True)

#alembic revision --autogenerate -m "initial migration"