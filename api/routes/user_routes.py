from fastapi import APIRouter
from fastapi.params import Depends
from auth_setup import (auth_backend, fastapi_users)
from api.schemas.contract_schemas import *

from models.contract_models import User


router = APIRouter(prefix='/users',
                   tags=['Users'])


# Suppliers and Customers Auth

router.include_router(
    fastapi_users.get_auth_router(auth_backend))

router.include_router(
    fastapi_users.get_register_router(UserAuthReadSchema, UserCreateSchema))


# Auth Routes

@router.get('/me', response_model=UserReadSchema)
async def get_me_student(user: User = Depends(fastapi_users.current_user())):
    return user
