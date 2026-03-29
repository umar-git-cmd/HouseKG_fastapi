from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Region
from mysite.database.schema import RegionOutSchema, RegionInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


region_router = APIRouter(prefix='/regions')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@region_router.post('/', response_model=RegionOutSchema)
async def region_post(region: RegionInputSchema, db: Session = Depends(get_db)):
    region_db = Region(**region.dict())
    db.add(region_db)
    db.commit()
    db.refresh(region_db)
    return region_db

@region_router.get('/', response_model=List[RegionOutSchema])
async def region_list(db: Session = Depends(get_db)):
    return db.query(Region).all()

@region_router.get('/{region_id}/', response_model=RegionOutSchema)
async def region_detail(region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(status_code=400, detail='region not found')
    return region_db

@region_router.put('/{region_id}/', response_model=RegionOutSchema)
async def region_update(region_id: int, region: RegionInputSchema, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(status_code=404, detail='region not found')
    for key, value in region.dict().items():
        setattr(region_db, key, value)
    db.commit()
    db.refresh(region_db)
    return region_db

@region_router.delete('/{region_id}/', response_model=dict)
async def region_delete(region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(status_code=400, detail='region not found')
    db.delete(region_db)
    db.commit()
    return {'message': 'deleted'}