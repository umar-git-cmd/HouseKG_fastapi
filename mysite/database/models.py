from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey, Enum, Date, DateTime, SmallInteger
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime


class RoleChoices(str, PyEnum):
    admin = 'admin'
    seller = 'seller'
    buyer = 'buyer'


class PropertyTypeChoices(str, PyEnum):
    apartment = 'Квартира'
    house = 'Дом'
    land = 'Участок'
    commercial = 'Коммерческая недвижимость'


class UserProfile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.buyer)
    date_registered: Mapped[date] = mapped_column(Date, default=date.today)

    properties: Mapped[List['Property']] = relationship(back_populates='seller', cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] = relationship(back_populates='author', cascade='all, delete-orphan')


class Region(Base):
    __tablename__ = 'region'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region_name: Mapped[str] = mapped_column(String)

    region_cities: Mapped[List['City']] = relationship(back_populates='region_city', cascade='all, delete-orphan')
    region_districts: Mapped[List['District']] = relationship(back_populates='region_district', cascade='all, delete-orphan')
    properties: Mapped[List['Property']] = relationship(back_populates='region', cascade='all, delete-orphan')


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String)
    region_id: Mapped[int] = mapped_column(ForeignKey('region.id'))

    region_city: Mapped['Region'] = relationship(back_populates='region_cities')
    properties: Mapped[List['Property']] = relationship(back_populates='city')


class District(Base):
    __tablename__ = 'district'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    district_name: Mapped[str] = mapped_column(String)
    region_id: Mapped[int] = mapped_column(ForeignKey('region.id'))

    region_district: Mapped['Region'] = relationship(back_populates='region_districts')
    properties: Mapped[List['Property']] = relationship(back_populates='district')


class Property(Base):
    __tablename__ = 'property'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    property_type: Mapped[PropertyTypeChoices] = mapped_column(Enum(PropertyTypeChoices))
    address: Mapped[str] = mapped_column(String(100))
    area: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    rooms: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    floor: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    total_floor: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    images: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    document: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    region_id: Mapped[int] = mapped_column(ForeignKey('region.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    district_id: Mapped[int] = mapped_column(ForeignKey('district.id'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))

    region: Mapped['Region'] = relationship(back_populates='properties')
    city: Mapped['City'] = relationship(back_populates='properties')
    district: Mapped['District'] = relationship(back_populates='properties')
    seller: Mapped['UserProfile'] = relationship(back_populates='properties')
    reviews: Mapped[List['Review']] = relationship(back_populates='property', cascade='all, delete-orphan')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating: Mapped[int] = mapped_column(SmallInteger)
    comment: Mapped[str] = mapped_column(Text)
    date_publication: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    author_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    property_id: Mapped[Optional[int]] = mapped_column(ForeignKey('property.id'), nullable=True)

    author: Mapped['UserProfile'] = relationship(back_populates='reviews')
    property: Mapped[Optional['Property']] = relationship(back_populates='reviews')
