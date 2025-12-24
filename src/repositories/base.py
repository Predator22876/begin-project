from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update


class BaseRepository:
    model = None
    schema: BaseModel = None
    
    def __init__(self, session):
        self.session = session
    
    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
            
        return [self.schema.model_validate(item, from_attributes= True) for item in result.scalars().all()]
    
    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
            
        item = result.scalars().one_or_none()
        if item is None:
            return None
        return self.schema.model_validate(item, from_attributes= True)
    
    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        item = result.scalars().one()
        return self.schema.model_validate(item, from_attributes= True)
    
    async def edit(self, data: BaseModel, is_patch: bool = False, **filter_by):
        edit_stmt = (
            update(self.model).
            filter_by(**filter_by).
            values(**data.model_dump(exclude_unset=is_patch))
        )
        await self.session.execute(edit_stmt)
        
    async def delete(self, **filter_by):
        delete_stmt = (
            delete(self.model).
            filter_by(**filter_by).
            returning(self.model)
        )
        
        result = await self.session.execute(delete_stmt)
        item = result.scalars().one()

        if item is None:
            raise HTTPException(status_code=404, detail="Отель не найден") 
        return self.schema.model_validate(item, from_attributes= True)
        