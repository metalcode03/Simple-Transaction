from typing import List

import bcrypt
from fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.util import asyncio


import models
from database import SessionLocal
from account.schemas import Transaction, TransactResponse, AccountBalance


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/account",
    tags=['Accounts']
)

@router.post("/create")
def create_account(account:AccountBalance, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    if current_user:
        account_user = db.query(models.Account).filter(models.Account.user_id == account.user_id).first()
        if account_user:
            return HTTPException(status_code=400, detail="Account already exist")
        else:
            obj = models.Account(user_id=account.user_id)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return "Account Registered Successfully"
    else:
        return "Please Login"

@router.post("/transaction/add")
def add_transaction(transaction: Transaction, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    if current_user:
        pass
        obj = models.Transfer(transaction)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return "Transaction Successful"
    else:
        return "Please Login"


@router.get("/transaction/history")
def get_transaction(transaction: Transaction, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    if current_user:
        return db.query(models.Transaction).all
    else:
        return "Please Login"


@router.get('/transaction/{id}', status_code=status.HTTP_200_OK)
def transaction_detail(id, response: Response, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    if current_user:
        details = db.query(models.Transfer).filter(
            models.Transfer.id == id).first()
        if not details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Transaction with the id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail': f"Transaction with the id {id} is not available"}
        return details
    else:
        return "Please Login"


@router.delete('/transaction/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db.query(models.Transer).filter(models.Transfer.id ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.put('/transaction/{id}')
def updated(id, request: Transaction, db: Session = Depends(get_db)):
    data = db.query(models.Transfer).filter(models.Transfer.id == id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" Content Not found")
    data.update(request)
    db.commit()
    return data.first()
