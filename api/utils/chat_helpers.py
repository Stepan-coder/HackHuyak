from datetime import datetime
from typing import List

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
            var ws = new WebSocket("ws://localhost:8000/api/agreements/chat?user_id=2");
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


async def save_message_history(data, current_msg_id, from_who,
                               chat, session):
    if data:
        current_msg = None

        if type(data) == dict:
           if data['type'] == 'form':
               current_msg = {'id': current_msg_id,
                              'from': from_who,
                              'text': data['text'],
                              'buttons': data['buttons'],
                              'type': 'form',
                              'created_datetime': f'{datetime.now()}'}

           elif data['type'] == 'save':
               current_msg = {'id': current_msg_id,
                              'from': from_who,
                              'text': data['type'],
                              'buttons': data['buttons'],
                              'type': 'form',
                              'created_datetime': f'{datetime.now()}'}

           else:
               current_msg = {'id': current_msg_id,
                              'from': from_who,
                              'text': data['text'],
                              'placeholder': data['placeholder'],
                              'type': 'input',
                              'created_datetime': f'{datetime.now()}'}


        elif type(data) == str:
            current_msg = {'id': current_msg_id, 'from': from_who, 'text': data,
                           'type': 'input', 'created_datetime': f'{datetime.now()}'}

        if len(chat.messages_history):
            new_hist = list(chat.messages_history)
            new_hist.append(current_msg)

            chat.messages_history = new_hist

        else:
            chat.messages_history = [current_msg]

        session.add(chat)

        await session.commit()
        await session.refresh(chat)

        return chat.messages_history


details = {'company_INN': 'ИНН', 'company_OGRN': 'ОГРН', 'company_KPP': 'КПП', 'company_adress': 'адрес',
           'company_index': 'индекс', 'company_fullname': 'Юридическое имя', 'bank': 'Банк', 'BIC': 'БИК', 'payment_account': 'Р/С',
           'correspondent_account': 'К/С'}