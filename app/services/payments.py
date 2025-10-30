from app.models import metodo_pago
from sqlalchemy.orm import Session

from app.crud import getEstadoPorNombre
from app.models.estado_pago import EstadoPago
from app.models.pago import Pago
from app.schemes import create_payment_out, create_payment_request


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

    estado_actual = db.query(EstadoPago).filter(EstadoPago.id == pago.estado_actual).first()
    if estado_actual and estado_actual.nombre_estado in estados_bloqueados:
        raise Exception(estados_bloqueados[estado_actual.nombre_estado])

    pago.estado_actual = estado_cancelado.id
    db.commit()

    print("Cancelando pago:", pago.id)

    return {"detail": "Pago cancelado correctamente."}

