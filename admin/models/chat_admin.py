from sqladmin import ModelView
from models.contract_models import Chat


class ChatAdmin(ModelView, model=Chat):
    column_list = [Chat.id]


