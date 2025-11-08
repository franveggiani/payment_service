from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.session import get_db
from app.schemes import (
    create_payment_method_req,
    create_payment_request,
    update_payment_method_req,
)
from app.services import payment_method
from app.services import payments


router = APIRouter()


@router.get("/")
def root():
    return payment_method.root_logic()


@router.post("/create_payment")
def create_payment(request: create_payment_request, db: Session = Depends(get_db)):
    return payments.create_payment_logic(request, db)

@router.get("/cancel_payment/{payment_id}")
def cancel_payment(payment_id: int, db: Session = Depends(get_db)):
    return payments.cancel_payment_logic(payment_id, db)

@router.post("/create_payment_method")
def create_payment_method(request: create_payment_method_req, db: Session = Depends(get_db)):
    return payment_method.create_payment_method_logic(request, db)

@router.get("/get_payment_methods/{usuario_id}")
def get_payment_methods(usuario_id: int, db: Session = Depends(get_db)):
    return payment_method.get_payment_methods_logic(usuario_id, db)

@router.patch("/update_payment_method/{pm_id}")
def update_payment_method(pm_id: int, request: update_payment_method_req, db: Session = Depends(get_db)):
    return payment_method.update_payment_method_logic(pm_id, request, db)

@router.delete("/delete_payment_method/{pm_id}")
def delete_payment_method(pm_id: int, db: Session = Depends(get_db)):
    return payment_method.delete_payment_method_logic(pm_id, db)