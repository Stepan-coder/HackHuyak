import os
from typing import List, Annotated

from fastapi import status, UploadFile, File, APIRouter, HTTPException, Form
from fastapi.params import Depends
from fastapi.responses import FileResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_async_session
from api.schemas.contract_schemas import *
from api.services.mailing import send_email_with_file
from auth_setup import fastapi_users

from models.contract_models import *
from settings import config_parameters

router = APIRouter(prefix='/contracts',
                   tags=['Contracts'])


# contract: Annotated[ContractCreateScheme, Form()]

@router.post('/create', response_model=ContractReadCreatedSchema)
async def create_contract(number: str, document_file: UploadFile = File(...), supplier_email: str = None,
                          customer_email: str = None, session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(fastapi_users.current_user())):
    if document_file.content_type != 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        raise HTTPException(status_code=400, detail='Документ должен быть в формате PDF!')

    file_location = os.path.join(config_parameters.CONTRACTS_DIR, document_file.filename)

    with open(file_location, "wb") as f:
        contents = await document_file.read()
        f.write(contents)

    customer_id = None
    supplier_id = None

    if user.role.role_type == 'customer':
        customer_id = user.id

        supplier_query = await session.execute(select(User).filter(User.email == supplier_email))
        supplier_id = supplier_query.scalars().first().id

    elif user.role.role_type == 'supplier':
        supplier_id = user.id

        customer_query = await session.execute(select(User).filter(User.email == customer_email))
        customer_id = customer_query.scalars().first().id

    contract_obj = Contract(number=number, supplier_id=supplier_id,
                            customer_id=customer_id, document_file=document_file.filename,
                            creator_id=user.id)

    session.add(contract_obj)
    await session.commit()

    return contract_obj


@router.get('/get/{contract_id}', response_model=ContractReadSchema)
async def get_contract(contract_id: int, session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(fastapi_users.current_user())):
    contract_query = await session.execute(select(Contract).filter(Contract.id == contract_id))
    contract = contract_query.scalars().first()

    if user.id not in [contract.customer_id, contract.supplier_id]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вы не имеете доступа к этому договору!')

    if contract is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Договор не найден!')

    return contract


@router.get('/get/{contract_id}/document')
async def get_contract_document(contract_id: int, session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(fastapi_users.current_user())):
    contract_query = await session.execute(select(Contract).filter(Contract.id == contract_id))
    contract = contract_query.scalars().first()

    if user.id not in [contract.customer_id, contract.supplier_id]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вы не имеете доступа к этому договору!')

    if contract is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Договор не найден!')

    document_path = f'{config_parameters.CONTRACTS_DIR}/{contract.document_file}'
    response = FileResponse(document_path, filename=contract.document_file)

    await send_email_with_file(subject=f'Документ №{contract.number}', recipient='belogurov.ivan@list.ru',
                               body='Отправка документа с Acmenra!', file=document_path)

    return response


@router.get('/get_all', response_model=List[ContractReadSchema])
async def get_all_contracts(session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(fastapi_users.current_user())):
    contract_query = await session.execute(select(Contract).filter(Contract.creator_id == user.id))
    contracts = contract_query.scalars().all()

    return contracts


@router.put('/get/{contract_id}', response_model=ContractReadSchema)
async def update_contract(contract_id: int, contract_update: ContractCreateScheme,
                  session: AsyncSession = Depends(get_async_session),
                  user: User = Depends(fastapi_users.current_user())):
    contract_query = await session.execute(select(Contract).filter(Contract.id == contract_id))
    contract = contract_query.scalars().first()

    if user.id not in [contract.customer_id, contract.supplier_id]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вы не имеете доступа к этому договору!')

    if contract is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Договор не найден!')

    for field, value in contract_update.dict(exclude_unset=True).items():
        setattr(contract, field, value)

    await session.commit()

    return contract


@router.delete('/delete/{practice_id}', response_model=dict)
async def delete_contract(contract_id: int, session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(fastapi_users.current_user())):
    contract_query = await session.execute(select(Contract).filter(Contract.id == contract_id))
    contract = contract_query.scalars().first()

    if user.id not in [contract.customer_id, contract.supplier_id]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вы не имеете доступа к этому договору!')

    if contract is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Договор не найден!')

    await session.delete(contract)
    await session.commit()

    return {'message': 'Договор успешно удалён!'}