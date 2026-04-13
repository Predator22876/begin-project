from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.post("")
async def create_facilities(facilities_data: FacilitiesAdd, db: DBDep):
    facilities = await db.facilities.add(facilities_data)
    await db.commit()

    # test_task.delay()

    return {"status": "ok", "data": facilities}


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()
