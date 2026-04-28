from src.schemas.facilities import FacilitiesAdd
from src.services.base import BaseService

class FacilityService(BaseService):
    async def create_facility(self, data: FacilitiesAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()

        # test_task.delay() # type: ignore
        return facility
    
    async def get_facilities(self):
        return await self.db.facilities.get_all()