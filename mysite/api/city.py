from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import City
from mysite.database.schema import CityInputSchema, CityOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List



city_router = APIRouter(prefix='/cities')



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@city_router.post('/', response_model=CityOutSchema)
async def city_post(city: CityInputSchema, db: Session = Depends(get_db)):
    city_db = City(**city.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.get('/', response_model=List[CityOutSchema])
async def city_list(db: Session = Depends(get_db)):
    return db.query(City).all()

@city_router.get('/{city_id}/', response_model=CityOutSchema)
async def city_detail(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=400, detail='city not found')
    return city_db

@city_router.put('/{city_id}/', response_model=CityOutSchema)
async def city_update(city_id: int, city: CityInputSchema, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=404, detail='city not found')
    for key, value in city.dict().items():
        setattr(city_db, key, value)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.delete('/{city_id}/', response_model=dict)
async def city_delete(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=400, detail='city not found')
    db.delete(city_db)
    db.commit()
    return {'message': 'deleted'}