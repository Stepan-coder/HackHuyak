from distutils.ccompiler import new_compiler

from fastapi import APIRouter, WebSocket
from fastapi.params import Depends
from fastapi.responses import HTMLResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typer.cli import state

from typing import List
from docworker.docreader import read_docx_in_paragraphs, read_table_in_paragraphs
from user_qa import get_answer
from NER import *
from docworker.templater import DocumentGenerator


from api.database import get_async_session, database
from api.schemas.contract_schemas import ChatReadSchema
from api.utils.chat_helpers import html as ws_html, save_message_history, details
from api.utils.fsm_new import graph

from api.utils.fsm_new import first_btn, second_btn
from auth_setup import fastapi_users

from models.contract_models import *


router = APIRouter(prefix='/agreements',
                   tags=['Agreements'])


@router.get('/')
async def get_chat():
    return HTMLResponse(ws_html)


@router.post('/chat/create', response_model=ChatReadSchema)
async def create_chat(session: AsyncSession = Depends(get_async_session)):
    chat_obj = Chat()

    session.add(chat_obj)
    await session.commit()

    return chat_obj


@router.websocket('/chat')
async def agreement_chat(websocket: WebSocket, user_id: int = None, session: AsyncSession = Depends(get_async_session),):
    await websocket.accept()

    user_query = await session.execute(select(User).filter(User.id == user_id))
    user = user_query.scalars().first()

    chat_query = await session.execute(select(Chat).filter(Chat.user_id == user.id))
    chat = chat_query.scalars().first()

    contract_new = {}

    current_msg_id = 1
    current_state = graph.get_node(1)

    if chat.messages_history != {}:
        if len(chat.messages_history):
            current_msg_id = chat.messages_history[-1]['id'] + 1

            await websocket.send_json(chat.messages_history)

    while True:
        data = await websocket.receive_text()

        if data:
            msg_history = await save_message_history(data, current_msg_id, 'user',
                                                     chat, session)
            current_msg_id += 1

            if data == 'доп':
                break

    current_msg_id += 1
    current_contract = None

    start_msg = eval(graph.get_node(1).attachment)

    await save_message_history(start_msg, current_msg_id, 'system',
                               chat, session)

    await websocket.send_json(start_msg)

    while True:
        data = await websocket.receive_text()

        if data:
            if not data.startswith('*'):
                await websocket.send_json('Промежуточный вопрос')
                continue

            state_attachment = eval(current_state.attachment)

            if state_attachment['type'] == 'input':
                if state_attachment['field'] == 'contract_number':
                    contract_query = await session.execute(select(Contract).filter(Contract.number == data[1:]))
                    contract = contract_query.scalars().first()

                    if contract:
                        current_contract = contract
                        paragraphs = read_docx_in_paragraphs(current_contract.document_file)
                        cells = read_table_in_paragraphs(current_contract.document_file)

                        for field, name in details:
                            contract_new[f'customer_{field}'] = get_answer(name, paragraphs)

                            contract_new[f'supplier_{field}'] = get_answer(name, paragraphs,)

                    else:
                        await websocket.send_json(state_attachment)
                        continue

                contract_new[state_attachment['field']] = data[1:]

                if 'main_to' in list(state_attachment.keys()):
                    current_state = graph.get_node(int(state_attachment['main_to'][1:]))

                else:
                    current_state = graph.get_node(list(graph.predict(current_state.id).values())[0])

            elif state_attachment['type'] == 'form':
                current_state = graph.get_node(int(data[1:]))

                if eval(current_state.attachment)['type'] == 'save':
                    current_contract.contract_content = contract_new
                    session.add(current_contract)

                    await session.commit()
                    await session.refresh(current_contract)

                    break

            await save_message_history(data, current_msg_id, 'user',
                                                     chat, session)

            system_msg = eval(current_state.attachment)
            await save_message_history(system_msg, current_msg_id, 'system',
                                       chat, session)

            await websocket.send_json(system_msg)

    DocumentGenerator.generate_document()

    await websocket.send_json(contract_new)
