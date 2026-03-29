from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum



class RoleChoices(str, Enum):
    admin = 'admin'
    seller = 'seller'
    buyer = 'buyer'


class PropertyTypeChoices(str, Enum):
    apartment = 'Квартира'
    house = 'Дом'
    land = 'Участок'
    commercial = 'Коммерческая недвижимость'



class RegionInputSchema(BaseModel):
    region_name: str

class RegionOutSchema(BaseModel):
    id: int
    region_name: str


class CityInputSchema(BaseModel):
    city_name: str
    region_id: int

class CityOutSchema(BaseModel):
    id: int
    city_name: str
    region_id: int



class DistrictInputSchema(BaseModel):
    district_name: str
    region_id: int

class DistrictOutSchema(BaseModel):
    id: int
    district_name: str
    region_id: int



class UserProfileInputSchema(BaseModel):
    username: str
    password: str
    avatar: Optional[str] = None
    phone_number: Optional[str] = None
    role: RoleChoices = RoleChoices.buyer



class UserProfileOutSchema(BaseModel):
    id: int
    username: str
    password: str
    avatar: Optional[str]
    phone_number: Optional[str]
    role: RoleChoices
    date_registered: date



class PropertyInputSchema(BaseModel):
    title: str
    description: str
    property_type: PropertyTypeChoices
    region_id: int
    city_id: int
    district_id: int
    address: str
    area: int
    price: int
    rooms: Optional[int] = None
    floor: Optional[int] = None
    total_floor: Optional[int] = None
    images: Optional[str] = None
    document: Optional[bool] = None


class PropertyOutSchema(BaseModel):
    id: int
    title: str
    description: str
    property_type: PropertyTypeChoices
    region: RegionOutSchema
    city: CityOutSchema
    district: DistrictOutSchema
    address: str
    area: int
    price: int
    rooms: Optional[int]
    floor: Optional[int]
    total_floor: Optional[int]
    images: Optional[str]
    document: Optional[bool]
    seller: UserProfileOutSchema

class ReviewOutSchema(BaseModel):
    id: int
    rating: int
    comment: str | None
    date_publication: datetime
    author_id: int
    property_id: int

class ReviewInputSchema(BaseModel):
    rating: int
    comment: str | None
    author_id: int
    property_id: int
