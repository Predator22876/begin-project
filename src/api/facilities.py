from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.services.facilities import FacilityService
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.post("")
async def create_facilities(facilities_data: FacilitiesAdd, db: DBDep):
    facility = await FacilityService(db).create_facility(facilities_data)
    return {"status": "ok", "data": facility}


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()
