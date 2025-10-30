from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from app.models.estado_pago import EstadoPago
from app.models.gateway_metodo_pago import GatewayMetodoPago
from app.models.marca_metodo_pago import MarcaMetodoPago
from app.models.metodo_pago import MetodoPago
from app.models.pago import Pago
from app.models.tipo_metodo_pago import TipoMetodoPago
from sqlalchemy.orm import Session
from app.session import get_db
from app.schemes import (
    create_payment_method_out,
    create_payment_method_req,
    create_payment_request,
    get_payment_method,
    update_payment_method_req,
)
from app.services.payments import cancel_payment_logic, create_payment_logic

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Hello World"}

@router.post("/create_payment")
def create_payment(request: create_payment_request, db: Session = Depends(get_db)):
    return create_payment_logic(request, db)

@router.post("/create_payment_method")
def create_payment_method(request: create_payment_method_req, db: Session = Depends(get_db)):
    if request.nro_tarjeta is not None and not request.nro_tarjeta.isdigit():
        raise HTTPException(status_code=400, detail="nro_tarjeta debe contener solo números.")

    metodo_pago: MetodoPago = MetodoPago(
        usuario_id=request.usuario_id,
        tipo_pago_id=request.tipo_pago_id,
        marca_pago_id=request.marca_pago_id,
        gateway_pago_id=request.gateway_pago_id,
        es_default=request.es_default,
        identificador_wallet=request.identificador_wallet,
        numero_tarjeta=request.nro_tarjeta,
        ultimos_cuatro_digitos=request.nro_tarjeta[-4:] if request.nro_tarjeta else None
    )

    if request.es_default == True:
        db.query(MetodoPago).filter(MetodoPago.es_default == True, MetodoPago.usuario_id == request.usuario_id).update({"es_default": False})

    db.add(metodo_pago)
    db.commit()

    return create_payment_method_out(
        id=metodo_pago.id,
        usuario_id=metodo_pago.usuario_id,
        tipo_pago_id=metodo_pago.tipo_pago_id,
        marca_pago_id=metodo_pago.marca_pago_id,
        gateway_pago_id=metodo_pago.gateway_pago_id,
        es_default=metodo_pago.es_default,
        identificador_wallet=metodo_pago.identificador_wallet,
        ultimos_cuatro_digitos=metodo_pago.ultimos_cuatro_digitos
    )

@router.get("/get_payment_methods/{usuario_id}")
def get_payment_methods(usuario_id: int, db: Session = Depends(get_db)):
    metodos_pago: list[MetodoPago] = db.query(MetodoPago).filter(MetodoPago.usuario_id == usuario_id, MetodoPago.fecha_hora_baja == None).all()

    response: list[get_payment_method] = []

    for metodo in metodos_pago:
        nombre_tipo_metodo = None
        nombre_marca_metodo = None
        nombre_gateway_metodo = None
        ultimos_cuatro_digitos_out = None

        if metodo.tipo_pago_id is not None:
            tipo_metodo: TipoMetodoPago = db.query(TipoMetodoPago).filter(TipoMetodoPago.id == metodo.tipo_pago_id).first()
            if tipo_metodo:
                nombre_tipo_metodo = tipo_metodo.nombre_metodo

        if metodo.marca_pago_id is not None:
            marca_metodo: MarcaMetodoPago = db.query(MarcaMetodoPago).filter(MarcaMetodoPago.id == metodo.marca_pago_id).first()
            if marca_metodo:
                nombre_marca_metodo = marca_metodo.nombre_marca

        if metodo.gateway_pago_id is not None:
            gateway_metodo: GatewayMetodoPago = db.query(GatewayMetodoPago).filter(GatewayMetodoPago.id == metodo.gateway_pago_id).first()
            if gateway_metodo:
                nombre_gateway_metodo = gateway_metodo.nombre_gateway

        if metodo.numero_tarjeta is not None:
            ultimos_cuatro_digitos_out = metodo.ultimos_cuatro_digitos
            
        response_detail = get_payment_method(
            id=metodo.id,
            usuario_id=metodo.usuario_id,
            tipo_pago=nombre_tipo_metodo,
            marca_pago=nombre_marca_metodo,
            gateway_pago=nombre_gateway_metodo,
            es_default=metodo.es_default,
            identificador_wallet=metodo.identificador_wallet,
            ultimos_cuatro_digitos=ultimos_cuatro_digitos_out
        )

        response.append(response_detail)

    return response

@router.patch("/update_payment_method/{pm_id}")
def update_payment_method(pm_id: int, request: update_payment_method_req, db: Session = Depends(get_db)):
    
    metodo_pago: MetodoPago = db.query(MetodoPago).filter(MetodoPago.id == pm_id).first()

    if request.nro_tarjeta is not None and not request.nro_tarjeta.isdigit():
        raise HTTPException(status_code=400, detail="nro_tarjeta debe contener solo números.")

    metodo_pago.tipo_pago_id = request.tipo_pago_id
    metodo_pago.marca_pago_id = request.marca_pago_id
    metodo_pago.gateway_pago_id = request.gateway_pago_id
    metodo_pago.es_default = request.es_default
    metodo_pago.identificador_wallet = request.identificador_wallet
    if request.nro_tarjeta:
        metodo_pago.numero_tarjeta = request.nro_tarjeta
        metodo_pago.ultimos_cuatro_digitos = request.nro_tarjeta[-4:]

    if request.es_default == True:
        db.query(MetodoPago).filter(MetodoPago.es_default == True, MetodoPago.usuario_id == metodo_pago.usuario_id).update({"es_default": False})

    db.commit()

    nombre_tipo_metodo = None
    nombre_marca_metodo = None
    nombre_gateway_metodo = None

    if metodo_pago.tipo_pago_id is not None:
        tipo_metodo: TipoMetodoPago = db.query(TipoMetodoPago).filter(TipoMetodoPago.id == metodo_pago.tipo_pago_id).first()
        if tipo_metodo:
            nombre_tipo_metodo = tipo_metodo.nombre_metodo

    if metodo_pago.marca_pago_id is not None:
        marca_metodo: MarcaMetodoPago = db.query(MarcaMetodoPago).filter(MarcaMetodoPago.id == metodo_pago.marca_pago_id).first()
        if marca_metodo:
            nombre_marca_metodo = marca_metodo.nombre_marca

    if metodo_pago.gateway_pago_id is not None:
        gateway_metodo: GatewayMetodoPago = db.query(GatewayMetodoPago).filter(GatewayMetodoPago.id == metodo_pago.gateway_pago_id).first()
        if gateway_metodo:
            nombre_gateway_metodo = gateway_metodo.nombre_gateway  

    return get_payment_method(
        id=metodo_pago.id,
        usuario_id=metodo_pago.usuario_id,
        tipo_pago=nombre_tipo_metodo,
        marca_pago=nombre_marca_metodo,
        gateway_pago=nombre_gateway_metodo,
        es_default=metodo_pago.es_default,
        identificador_wallet=metodo_pago.identificador_wallet,
        ultimos_cuatro_digitos=metodo_pago.ultimos_cuatro_digitos
    )


@router.delete("/delete_payment_method/{pm_id}")
def delete_payment_method(pm_id: int, db: Session = Depends(get_db)):
    metodo_pago: MetodoPago | None = db.query(MetodoPago).filter(MetodoPago.id == pm_id).first()

    if metodo_pago is None:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado.")

    if metodo_pago.es_default:
        raise HTTPException(status_code=400, detail="No se puede eliminar un método de pago por defecto.")

    metodo_pago.fecha_hora_baja = datetime.utcnow()
    db.commit()

    return {"detail": "Método de pago dado de baja correctamente."}


@router.get("/cancel_payment/{payment_id}")
def cancel_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        return cancel_payment_logic(payment_id, db)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
