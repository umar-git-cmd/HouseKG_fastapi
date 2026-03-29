from mysite.database.models import *
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.username, UserProfile.username]


class RegionAdmin(ModelView, model=Region):
    column_list = [Region.id, Region.id]
