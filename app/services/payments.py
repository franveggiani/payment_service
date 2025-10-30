import os
from datetime import datetime

from app.models import metodo_pago
from app.models import estado_pago
from sqlalchemy.orm import Session

from app.crud import getEstadoPorNombre
from app.models.estado_pago import EstadoPago
from app.models.pago import Pago
from app.schemes import create_payment_out, create_payment_request
from app.rabbit_publisher import publish_json_background

STATUS_QUEUE = os.getenv("PAYMENTS_STATUS_QUEUE", "payments_status")


def create_payment_logic(request: create_payment_request, db: Session) -> create_payment_out:
    estado_pago = getEstadoPorNombre("En Proceso", db)
    if estado_pago is None:
        raise Exception("Estado pendiente no encontrado")

    payment = Pago(
        nro_cuenta=request.nro_cuenta,
        monto_pagado=request.monto_pagado,
        estado_actual=estado_pago.id,
        orden_id=request.order_id,
        metodo_pago_id=request.metodo_pago_id
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Publicar evento de nuevo pago / cambio de estado inicial
    publish_json_background(
        STATUS_QUEUE,
        {
            "event": "payment_status_changed",
            "payment_id": payment.id,
            "order_id": payment.orden_id,
            "previous_status": None,
            "new_status": estado_pago.nombre_estado,
            "changed_at": datetime.utcnow().isoformat(),
        },
    )

    return create_payment_out(
        nro_cuenta=payment.nro_cuenta,
        monto_pagado=payment.monto_pagado,
        estado=estado_pago.nombre_estado,
    )


def cancel_payment_logic(payment_id: int, db: Session) -> dict:
    pago: Pago | None = db.query(Pago).filter(Pago.id == payment_id).first()
    if pago is None:
        raise Exception("Pago no encontrado.")

    estado_cancelado: EstadoPago | None = db.query(EstadoPago).filter(EstadoPago.nombre_estado == "Cancelado").first()
    if estado_cancelado is None:
        raise Exception("Estado cancelado no encontrado.")

    estados_bloqueados = {
        "Cancelado": "El pago ya fue cancelado.",
        "Realizado": "El pago ya fue realizado.",
        "Fallido": "El pago ya fue fallido.",
    }

    estado_anterior: EstadoPago | None = db.query(EstadoPago).filter(EstadoPago.id == pago.estado_actual).first()
    if estado_anterior and estado_anterior.nombre_estado in estados_bloqueados:
        raise Exception(estados_bloqueados[estado_anterior.nombre_estado])

    pago.estado_actual = estado_cancelado.id
    db.commit()

    # Publicar evento de cambio de estado (async, no bloqueante)
    publish_json_background(
        STATUS_QUEUE,
        {
            "event": "payment_status_changed",
            "payment_id": pago.id,
            "order_id": pago.orden_id,
            "previous_status": estado_anterior.nombre_estado if estado_anterior else None,
            "new_status": estado_cancelado.nombre_estado,
            "changed_at": datetime.utcnow().isoformat(),
        },
    )

    return {"detail": "Pago cancelado correctamente."}

def change_payment_status_logic(payment_id: int, status_id: int, db: Session):
    pago: Pago | None = db.query(Pago).filter(Pago.id == payment_id).first()
    if pago is None:
        raise Exception("Pago no encontrado.")

    nuevo_estado: EstadoPago | None = db.query(EstadoPago).filter(EstadoPago.id == status_id).first()
    if nuevo_estado is None:
        raise Exception("Estado destino no encontrado.")

    estado_anterior: EstadoPago | None = db.query(EstadoPago).filter(EstadoPago.id == pago.estado_actual).first()

    if nuevo_estado.nombre_estado == "Cancelado":
        raise Exception("Para cancelar use el endpoint específico de cancelación.")

    if not estado_anterior or estado_anterior.nombre_estado != "En Proceso":
        raise Exception("Solo se puede actualizar un pago en estado 'En Proceso'.")

    if nuevo_estado.nombre_estado not in ("Realizado", "Fallido"):
        raise Exception("Nuevo estado inválido. Debe ser 'Realizado' o 'Fallido'.")

    pago.estado_actual = nuevo_estado.id
    db.commit()

    publish_json_background(
        STATUS_QUEUE,
        {
            "event": "payment_status_changed",
            "payment_id": pago.id,
            "order_id": pago.orden_id,
            "previous_status": estado_anterior.nombre_estado if estado_anterior else None,
            "new_status": nuevo_estado.nombre_estado,
            "changed_at": datetime.utcnow().isoformat(),
        },
    )

    return {"detail": "Estado de pago actualizado correctamente"}
