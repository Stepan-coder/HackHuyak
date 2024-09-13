import os
import json

from typing import List, Annotated
from datetime import datetime

from fastapi import status, APIRouter, WebSocket
from fastapi.params import Depends
from fastapi.responses import FileResponse, HTMLResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_async_session
from api.utils.fsm import graph
from auth_setup import fastapi_users

from models.contract_models import *
from settings import config_parameters

router = APIRouter(prefix='/agreements',
                   tags=['Agreements'])



html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/api/agreements/chat");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get('/')
async def get_chat():
    return HTMLResponse(html)


@router.websocket('/chat')
async def agreement_chat(websocket: WebSocket):
    await websocket.accept()

    messages_history = []
    current_msg_id = 1

    while True:
        data = await websocket.receive_text()

        if data != '' or data != None:
            messages_history.append({'id': current_msg_id,
                                     'from': 'user',
                                     'text': data,
                                     'created_datetime': datetime.now()})

            await websocket.send_json(f'Ответ на сообщение {current_msg_id} - {data}')

            current_msg_id += 1


# @router.websocket('/chat')
# async def agreement_chat(websocket: WebSocket,
#                              session: AsyncSession = Depends(get_async_session),
#                              user: User = Depends(fastapi_users.current_user())):
#     await websocket.accept()
#
#     agreement_new = {}
#     messages_history = []
#     states_history = []
#
#     current_msg_id = 1
#     current_state = None
#     states_json = None
#
#     with open(f'{config_parameters.ROOT_DIR}fsm_attachments.json', 'r') as fsm_json:
#          states_json = json.load(json.load(fsm_json))
#
#     while True:
#         data = await websocket.receive_text()
#
#         if data != '' or data != None:
#             if data == 'доп соглашение':
#                 messages_history.append({'id': current_msg_id,
#                                          'from': 'user',
#                                          'text': data,
#                                          'created_datetime': datetime.now()})
#
#                 for id in graph.predict(1).values():
#                     for state in states_json:
#                         if state['id'] == id:
#                             current_state = state
#
#                             break
#                     break
#
#                 current_msg_id += 1
#                 system_message = {'id': current_msg_id,
#                                   'from': 'system',
#                                   'text': current_state['attachment'],
#                                   'created_datetime': datetime.now()}
#
#                 await websocket.send_json(system_message)
#                 break
#
#     while True:
#         data = await websocket.receive_text()
#
#         if data != '' and data:
#             if data == 'break':
#                 break
#
#             if current_state['type'] == 'input':
#                 messages_history.append({'id': current_msg_id,
#                                          'from': 'user',
#                                          'text': data,
#                                          'created_datetime': datetime.now()})
#
#                 agreement_new[current_state['field']] = data
#
#         await websocket.send_text(f"Message text was: {data}")