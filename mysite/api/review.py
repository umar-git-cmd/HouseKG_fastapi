from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Review
from mysite.database.schema import ReviewInputSchema, ReviewOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

review_router = APIRouter(prefix='/reviews')


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.post('/', response_model=ReviewOutSchema)
async def review_post(review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.get('/', response_model=List[ReviewOutSchema])
async def review_list(db: Session = Depends(get_db)):
    return db.query(Review).all()

@review_router.get('/{review_id}/', response_model=ReviewOutSchema)
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=400, detail='review not found')
    return review_db

@review_router.put('/{review_id}/', response_model=ReviewOutSchema)
async def review_update(review_id: int, review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail='review not found')
    for key, value in review.dict().items():
        setattr(review_db, key, value)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.delete('/{review_id}/', response_model=dict)
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=400, detail='review not found')
    db.delete(review_db)
    db.commit()
    return {'message': 'deleted'}