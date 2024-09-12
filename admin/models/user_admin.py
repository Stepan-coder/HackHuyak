from sqladmin import ModelView
from models.contract_models import User, Role


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.reg_number]


class RoleAdmin(ModelView, model=Role):
    column_list = [Role.id, Role.name]