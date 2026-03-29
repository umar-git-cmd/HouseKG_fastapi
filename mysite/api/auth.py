from fastapi import APIRouter, HTTPException, Depends
from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile
from mysite.database.schema import UserProfileInputSchema
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import bcrypt

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


@auth_router.post('/register/', response_model=dict)
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if user_db:
        raise HTTPException(status_code=400, detail='Есть такой юзер')

    user_data = UserProfile(
        username=user.username,
        phone_number=user.phone_number,
        password=get_password_hash(user.password)
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'message': 'зареган успешно'}