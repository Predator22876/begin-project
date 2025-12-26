from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.post("")
async def create_facilities(
    facilities_data: FacilitiesAdd,
    db: DBDep
):
    facilities = await db.facilities.add(facilities_data)
    await db.commit()

    return {"status": "ok", "data": facilities}

@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()
