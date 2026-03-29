from fastapi import FastAPI
import uvicorn
from mysite.api import user, region, city, district, property, review, auth
from mysite.admin.setup import setup_admin
houseKG_app_fastapi = FastAPI()

houseKG_app_fastapi.include_router(user.user_router)
houseKG_app_fastapi.include_router(region.region_router)
houseKG_app_fastapi.include_router(city.city_router)
houseKG_app_fastapi.include_router(district.district_router)
houseKG_app_fastapi.include_router(property.property_router)
houseKG_app_fastapi.include_router(review.review_router)
houseKG_app_fastapi.include_router(auth.auth_router)
setup_admin(houseKG_app_fastapi)
if __name__ == '__main__':
    uvicorn.run(houseKG_app_fastapi, host='127.0.0.1', port=8000)

