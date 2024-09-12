from datetime import datetime, date
from typing import Optional, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from api.database import Base
from sqlalchemy.orm import relationship, Mapped
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

    document_name: Mapped[str] = Column(String, nullable=False)
    document_content = Column(LargeBinary, nullable=False)

    customer_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=True)
    customer: Mapped[Optional['User']] = relationship('User', foreign_keys='[Contract.customer_id]',
                                                      lazy='selectin')

    supplier_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=True)
    supplier: Mapped[Optional['User']] = relationship('User', foreign_keys='[Contract.supplier_id]',
                                                      lazy='selectin')

    creator_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=True)
    creator: Mapped[Optional['User']] = relationship('User', foreign_keys='[Contract.creator_id]',
                                                     lazy='selectin')

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

    document_name: Mapped[str] = Column(String, nullable=False)
    document_content = Column(LargeBinary, nullable=False)

    messages_history: Mapped[List[dict]] = Column(JSON, nullable=True)
    states_history: Mapped[List[dict]] = Column(JSON, nullable=True)

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