from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Property
from mysite.database.schema import PropertyOutSchema, PropertyInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List



property_router = APIRouter(prefix='/properties')



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




property_router.post('/', response_model=PropertyOutSchema)
async def property_post(property: PropertyInputSchema, db: Session = Depends(get_db)):
    property_db = Property(**property.dict())
    db.add(property_db)
    db.commit()
    db.refresh(property_db)
    return property_db

@property_router.get('/', response_model=List[PropertyOutSchema])
async def property_list(db: Session = Depends(get_db)):
    return db.query(Property).all()

@property_router.get('/{property_id}/', response_model=PropertyOutSchema)
async def property_detail(property_id: int, db: Session = Depends(get_db)):
    property_db = db.query(Property).filter(Property.id == property_id).first()
    if not property_db:
        raise HTTPException(status_code=400, detail='property not found')
    return property_db

@property_router.put('/{property_id}/', response_model=PropertyOutSchema)
async def property_update(property_id: int, property: PropertyInputSchema, db: Session = Depends(get_db)):
    property_db = db.query(Property).filter(Property.id == property_id).first()
    if not property_db:
        raise HTTPException(status_code=404, detail='property not found')
    for key, value in property.dict().items():
        setattr(property_db, key, value)
    db.commit()
    db.refresh(property_db)
    return property_db

@property_router.delete('/{property_id}/', response_model=dict)
async def property_delete(property_id: int, db: Session = Depends(get_db)):
    property_db = db.query(Property).filter(Property.id == property_id).first()
    if not property_db:
        raise HTTPException(status_code=400, detail='property not found')
    db.delete(property_db)
    db.commit()
    return {'message': 'deleted'}