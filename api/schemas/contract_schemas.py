from datetime import datetime
from typing import Optional, List

from fastapi import UploadFile, File
from fastapi_users import schemas
from pydantic import BaseModel


class SpecificationCreateSchema(BaseModel):
    document_name: str


class SpecificationReadDetailSchema(BaseModel):
    id: int

    document_name: str
    agreement_id: int


class SpecificationReadSchema(BaseModel):
    id: int
    document_name: str


class AgreementReadDetailSchema(BaseModel):
    id: int
    contract_id: int
    contract: Optional['ContractReadSchema'] = None

    specification_id: int
    specification: Optional['SpecificationReadSchema'] = None

    messages_history: list[dict]
    states_history: list[dict]

    document_name: str

    created: bool
    created_date: bool


class AgreementReadSchema(BaseModel):
    id: int
    contract_id: int

    document_name: str
    created: bool
    created_date: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class AgreementCreateSchema(BaseModel):
    contract_id: int
    document_name: str

    class Config:
        from_attributes = True
        populate_by_name = True


class ContractCreateScheme(BaseModel):
    number: str
    from_date: Optional[datetime] = None

    document_file: UploadFile = File(...)

    supplier_email: Optional[str] = None
    customer_email: Optional[str] = None


class ContractReadSchema(BaseModel):
    id: int

    number: str
    customer_id: int
    customer: Optional['UserReadSchema'] = None

    document_name: str

    supplier_id: int
    supplier: Optional['UserReadSchema'] = None

    creator_id: int

    agreements: Optional[List['AgreementReadSchema']]

    class Config:
        from_attributes = True
        populate_by_name = True


class ContractReadCreatedSchema(BaseModel):
    id: int
    number: str
    document_name: str

    class Config:
        from_attributes = True
        populate_by_name = True


class RoleReadSchema(BaseModel):
    id: int
    name: str
    role_type: str


class UserReadSchema(BaseModel):
    id: int
    email: str

    reg_number: str
    reg_date: datetime
    reg_authority: str
    loc_address: str

    role: RoleReadSchema
    role_id: int

    supplier_contracts: Optional[List['ContractReadSchema']] = None
    customer_contracts: Optional[List['ContractReadSchema']] = None

    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True
        populate_by_name = True


class UserAuthReadSchema(schemas.BaseUser[int]):
    id: int
    email: str

    reg_number: str
    reg_date: datetime
    reg_authority: str
    loc_address: str

    role: Optional[RoleReadSchema] = None

    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True
        populate_by_name = True


class UserCreateSchema(schemas.BaseUserCreate):
    email: str

    reg_number: str
    reg_date: Optional[datetime] = None
    reg_authority: str
    loc_address: str

    password: str

    role_id: Optional[int] = None

    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

class RoleCreateScheme(BaseModel):
    name: str
    role_type: str