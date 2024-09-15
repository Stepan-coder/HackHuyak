from datetime import datetime, date
from typing import Optional, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from pygments.lexer import default

from sqlalchemy import event
from api.database import Base
from sqlalchemy.orm import relationship, Mapped, Session
from sqlalchemy import (Column, Integer, String, TIMESTAMP, ForeignKey, DATE,
                        Boolean, Text, DATE, Table, JSON, LargeBinary)


class Role(Base):
    __tablename__ = 'role'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, unique=True, nullable=False)
    role_type: Mapped[str] = Column(String, unique=True, nullable=False)

    users: Mapped[Optional[List['User']]] = relationship('User', back_populates='role', lazy='selectin')

    def __str__(self):
        return self.name


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(String, unique=True, nullable=False)

    reg_number: Mapped[str] = Column(String, unique=True, nullable=False)
    reg_date: Mapped[date] = Column(DATE, default=datetime.now)
    reg_authority: Mapped[str] = Column(Text, nullable=False)
    loc_address: Mapped[str] = Column(Text, nullable=False)

    # chat: Mapped[Optional['Chat']] = relationship('Chat', back_populates='user',
    #                                               uselist=False)

    registered_at: Mapped[datetime] = Column(TIMESTAMP, default=datetime.utcnow)

    role_id: Mapped[int] = Column(Integer, ForeignKey('role.id'), nullable=True)
    role: Mapped[Optional['Role']] = relationship('Role', back_populates='users', lazy='selectin')

    hashed_password: str = Column(String(length=1024), nullable=False)

    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    def __str__(self):
        return self.email


class Contract(Base):
    __tablename__ = 'contract'

    id: Mapped[int] = Column(Integer, primary_key=True)

    number: Mapped[str] = Column(String, unique=True)
    from_date: Mapped[date] = Column(DATE, default=datetime.now)

    document_file: Mapped[str] = Column(String, nullable=True)
    # document_content = Column(LargeBinary, nullable=False)

    customer_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=True)
    customer: Mapped[Optional['User']] = relationship('User', foreign_keys='[Contract.customer_id]',
                                                      lazy='selectin')

    supplier_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=True)
    supplier: Mapped[Optional['User']] = relationship('User', foreign_keys='[Contract.supplier_id]',
                                                      lazy='selectin')

    creator_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=True)
    creator: Mapped[Optional['User']] = relationship('User', foreign_keys='[Contract.creator_id]',
                                                     lazy='selectin')

    contract_content: Mapped[List[dict]] = Column(JSON, default={}, nullable=True)

    agreements: Mapped[Optional[List['Agreement']]] = relationship('Agreement',
                                                                          back_populates='contract', lazy='selectin')

    def __str__(self):
        return self.id


class Agreement(Base):
    __tablename__ = 'agreement'

    id: Mapped[int] = Column(Integer, primary_key=True)

    contract_id: Mapped[int] = Column(Integer, ForeignKey('contract.id'), nullable=True)
    contract: Mapped[Optional['Contract']] = relationship('Contract', back_populates='agreements',
                                                          lazy='selectin')

    specification: Mapped[Optional['Specification']] = relationship('Specification',
                                                                    back_populates='agreement', lazy='selectin')

    chat_id: Mapped[int] = Column(Integer, ForeignKey('chat.id'), nullable=True)
    chat: Mapped[Optional['Chat']] = relationship('Chat', back_populates='agreements',
                                                          lazy='selectin')

    document_name: Mapped[str] = Column(String, nullable=False)
    document_content = Column(LargeBinary, nullable=False)

    created: Mapped[bool] = Column(Boolean, default=False)
    created_date: Mapped[datetime] = Column(DATE, default=datetime.now)

    def __str__(self):
        return self.id


class Specification(Base):
    __tablename__ = 'specification'

    id: Mapped[int] = Column(Integer, primary_key=True)

    agreement_id: Mapped[int] = Column(Integer, ForeignKey('agreement.id'), nullable=False)
    agreement: Mapped[Optional['Agreement']] = relationship('Agreement', back_populates='specification',
                                                          lazy='selectin')

    document_name: Mapped[str] = Column(String, nullable=False)
    document_content = Column(LargeBinary, nullable=False)

    created_date: Mapped[datetime] = Column(DATE, default=datetime.now)

    def __str__(self):
        return self.id


class Chat(Base):
    __tablename__ = 'chat'

    id: Mapped[int] = Column(Integer, primary_key=True)

    messages_history: Mapped[List[dict]] = Column(JSON, default={}, nullable=True)
    states_history: Mapped[List[dict]] = Column(JSON, default={}, nullable=True)

    user_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=True)
    user: Mapped[Optional['User']] = relationship('User', uselist=False)

    agreements: Mapped[Optional[List['Agreement']]] = relationship('Agreement',
                                                                   back_populates='chat', lazy='selectin')

    def __str__(self):
        return self.id


@event.listens_for(User, 'after_insert')
def create_chat(mapper, connection, target: User):
    session: Session = Session(bind=connection)
    new_chat = Chat(user_id=target.id)

    session.add(new_chat)
    session.commit()

    # @router.websocket('/chat')
    # async def agreement_chat(websocket: WebSocket, user_id: int = None, session: AsyncSession = Depends(get_async_session),):
    #     await websocket.accept()
    #
    #     user_query = await session.execute(select(User).filter(User.id == user_id))
    #     user = user_query.scalars().first()
    #
    #     chat_query = await session.execute(select(Chat).filter(Chat.user_id == user.id))
    #     chat = chat_query.scalars().first()
    #
    #     contract_new = {}
    #
    #     current_msg_id = 1
    #     current_state = graph.get_node(1)
    #
    #     if chat.messages_history != {}:
    #         if len(chat.messages_history):
    #             current_msg_id = chat.messages_history[-1]['id'] + 1
    #
    #             await websocket.send_json(chat.messages_history)
    #
    #     while True:
    #         data = await websocket.receive_text()
    #
    #         if data:
    #             msg_history = await save_message_history(data, current_msg_id, 'user',
    #                                                      chat, session)
    #             current_msg_id += 1
    #
    #             if data == 'доп':
    #                 break
    #
    #     current_msg_id += 1
    #     start_msg = eval(graph.get_node(1).attachment)
    #     await save_message_history(start_msg, current_msg_id, 'system',
    #                                chat, session)
    #     await websocket.send_json(start_msg)
    #
    #     contract = None
    #
    #     while True:
    #         data = await websocket.receive_text()
    #
    #         if data:
    #             state_attachment = eval(current_state.attachment)
    #
    #             if state_attachment['type'] == 'input':
    #                 if state_attachment['field'] == 'contract_number':
    #                     contract_query = await session.execute(select(Contract).filter(Contract.number == data and Contract.creator.id == user.id))
    #                     contracts = contract_query.scalars()
    #
    #                     if len(contracts.all()) == 0:
    #                         await websocket.send_json(state_attachment)
    #                         continue
    #
    #                     else:
    #                         contract = contracts.first()
    #
    #                 contract_new[state_attachment['field']] = data
    #
    #                 if 'main_to' in list(state_attachment.keys()):
    #                     current_state = graph.get_node(state_attachment['main_to'])
    #
    #                 else:
    #                     current_state = graph.get_node(list(graph.predict(current_state.id).values())[0])
    #
    #             elif state_attachment['type'] == 'form':
    #                 current_state = graph.get_node(int(data))
    #
    #                 if eval(current_state.attachment)['type'] == 'save':
    #                     new_contract_content = contract.contract_content
    #
    #                     for key, value in contract_new:
    #                         new_contract_content[key] = value
    #
    #                     contract.contract_content = new_contract_content
    #                     session.add(contract)
    #
    #                     await session.commit()
    #                     await session.refresh(contract_new)
    #
    #                     break
    #
    #             await save_message_history(data, current_msg_id, 'user',
    #                                                      chat, session)
    #
    #             system_msg = eval(current_state.attachment)
    #             await save_message_history(system_msg, current_msg_id, 'system',
    #                                        chat, session)
    #
    #             await websocket.send_json(system_msg)
    #
    #     await websocket.send_json(contract_new)
