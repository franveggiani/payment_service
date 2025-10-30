from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.session import get_db
from app.models.estado_pago import EstadoPago

def getEstadoPorId(id, db: Session = Depends(get_db)):
    try:
        return db.query(EstadoPago).filter(EstadoPago.id == id).first()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
def getEstadoPorNombre(nombre: str, db: Session = Depends(get_db)):
    try:
        return db.query(EstadoPago).filter(EstadoPago.nombre_estado == nombre).first()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)    