from typing import Optional
from pydantic import BaseModel

class Transaction(BaseModel):
    type: str
    origin: str
    destination: str
    amount: int
    

class AccountBalance(BaseModel):
    balance: int
    user_id: int
    

class TransactResponse(BaseModel):
    type: str
    origin: str
    destination: str
