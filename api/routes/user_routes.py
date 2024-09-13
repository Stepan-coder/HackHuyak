from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_async_session
from auth_setup import (auth_backend, fastapi_users)
from api.schemas.contract_schemas import *

from models.contract_models import User, Role

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


@router.post('/roles/create', response_model=RoleReadSchema)
async def create_role(role: RoleCreateScheme,
                      session: AsyncSession = Depends(get_async_session)):
    role_obj = Role(name=role.name, role_type=role.role_type)

    session.add(role_obj)
    await session.commit()

    return role_obj