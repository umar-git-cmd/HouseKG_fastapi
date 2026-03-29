from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import District
from mysite.database.schema import DistrictOutSchema, DistrictInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

district_router = APIRouter(prefix='/districts')


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@district_router.post('/', response_model=DistrictOutSchema)
async def district_post(district: DistrictInputSchema, db: Session = Depends(get_db)):
    district_db = District(**district.dict())
    db.add(district_db)
    db.commit()
    db.refresh(district_db)
    return district_db

@district_router.get('/', response_model=List[DistrictOutSchema])
async def district_list(db: Session = Depends(get_db)):
    return db.query(District).all()

@district_router.get('/{district_id}/', response_model=DistrictOutSchema)
async def district_detail(district_id: int, db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id == district_id).first()
    if not district_db:
        raise HTTPException(status_code=400, detail='district not found')
    return district_db

@district_router.put('/{district_id}/', response_model=DistrictOutSchema)
async def district_update(district_id: int, district: DistrictInputSchema, db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id == district_id).first()
    if not district_db:
        raise HTTPException(status_code=404, detail='district not found')
    for key, value in district.dict().items():
        setattr(district_db, key, value)
    db.commit()
    db.refresh(district_db)
    return district_db

@district_router.delete('/{district_id}/', response_model=dict)
async def district_delete(district_id: int, db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id == district_id).first()
    if not district_db:
        raise HTTPException(status_code=400, detail='district not found')
    db.delete(district_db)
    db.commit()
    return {'message': 'deleted'}