import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy.types as types
from sqlalchemy.sql import func

Base = declarative_base()
metadata = Base.metadata



class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class User(Base):
    __tablename__ = "User"

    id = Column(Integer,  index=True,  primary_key=True, autoincrement=True)
    name = Column(String(200), index=True, nullable=True)
    number = Column(String(100), index=True, nullable=False)
    email = Column(String(250),primary_key=True, index=True)
    address = Column(String(250), index=True, nullable=False)
    password = Column(String(2500), index=True)
    accounts = relationship("Account", back_populates="user")
    transfer = relationship("Transfer", back_populates="user")
    

class Account(Base):
    __tablename__ = "Account"
    
    id = Column(Integer,  index=True,  primary_key=True, autoincrement=True)
    balance = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="accounts")
    created_date = Column(DateTime(timezone=True), server_default=func.now())

class Transfer(Base):
    __tablename__ = "Transfer"
    id = Column(Integer,  index=True,  primary_key=True, autoincrement=True)
    amount = Column(Integer)
    transfer_type = Column(
        ChoiceType({"children": "children", "adult": "adult", "tall": "tall"}), nullable=False
    )
    origin = Column(String(2500))
    destination = Column(String(2500))
    created_date = Column(DateTime(timezone=True), server_default=func.now())


class Otp(Base):
    __tablename__ = "Otp"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(259), index=True)
    otp = Column(Integer, index=True, nullable=False)
    status = Column(String(259), index=True, default=True)


class Admin(Base):
    __tablename__ = "Admin"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(250), index=True, nullable=True)
    password = Column(String(2500), index=True)
