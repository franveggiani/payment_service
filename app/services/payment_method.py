from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemes import (
    create_payment_method_out,
    create_payment_method_req,
    create_payment_request,
    get_payment_method,
    update_payment_method_req,
)
from app.services.payments import cancel_payment_logic, create_payment_logic
from app.models.metodo_pago import MetodoPago
from app.models.tipo_metodo_pago import TipoMetodoPago
from app.models.marca_metodo_pago import MarcaMetodoPago
from app.models.gateway_metodo_pago import ProveedorBilletera
from app.models.metodo_pago_tarjeta import MetodoPagoTarjeta
from app.models.metodo_pago_billetera import MetodoPagoBilletera
from app.models.banco import Banco


def root_logic() -> dict:
    return {"message": "Hello World"}


def create_payment_logic_controller(request: create_payment_request, db: Session):
    return create_payment_logic(request, db)


def create_payment_method_logic(request: create_payment_method_req, db: Session):
    # Validaciones base
    tipo: TipoMetodoPago | None = db.query(TipoMetodoPago).filter(TipoMetodoPago.id == request.tipo_pago_id).first()
    if not tipo:
        raise HTTPException(status_code=400, detail="Tipo de método de pago inválido.")

    tipo_nombre = tipo.nombre_metodo.lower()
    is_billetera = tipo_nombre == "billetera"
    is_tarjeta = tipo_nombre in ("debito", "débito", "credito", "crédito")

    if is_tarjeta:
        # Campos requeridos para tarjeta
        missing = []

        if not request.marca_pago_id:
            missing.append("marca_pago_id")
        if not request.nro_tarjeta:
            missing.append("nro_tarjeta")
        if not request.nombre_titular:
            missing.append("nombre_titular")
        if not request.fecha_vencimiento:
            missing.append("fecha_vencimiento")
        if not request.banco_id:
            missing.append("banco_id")

        if missing:
            raise HTTPException(status_code=400, detail=f"Faltan campos de tarjeta: {', '.join(missing)}")
        if not request.nro_tarjeta.isdigit():
            raise HTTPException(status_code=400, detail="nro_tarjeta debe contener solo números.")

        # Me quedo con los últimos 4 dígitos
        last4 = request.nro_tarjeta[-4:]

        # Me fijo si hay un metodo_pago_detalle que tenga las mismas características que el nuevo
        detalle_existente: MetodoPagoTarjeta | None = (
            db.query(MetodoPagoTarjeta)
            .filter(
                MetodoPagoTarjeta.marca_pago_id == request.marca_pago_id,
                MetodoPagoTarjeta.ultimos_cuatro_digitos == last4,
                MetodoPagoTarjeta.fecha_vencimiento == request.fecha_vencimiento,
                MetodoPagoTarjeta.banco_id == request.banco_id,
            )
            .first()
        )

        # Busco su metodo de pago asociado
        metodo_existente: MetodoPago | None = None
        if detalle_existente:
            metodo_existente = (
                db.query(MetodoPago)
                .filter(
                    MetodoPago.usuario_id == request.usuario_id,
                    MetodoPago.tipo_pago_id == request.tipo_pago_id,
                    MetodoPago.metodo_pago_detalle_id == detalle_existente.id,
                )
                .first()
            )

        # Si encuento un metodo existente, le doy de alta
        if metodo_existente:
            if metodo_existente.fecha_hora_baja is not None:
                metodo_existente.fecha_hora_baja = None
            if detalle_existente.fecha_hora_baja is not None:
                detalle_existente.fecha_hora_baja = None

            # detalle_existente.numero_tarjeta = request.nro_tarjeta
            detalle_existente.nombre_titular = request.nombre_titular

            # Si este nuevo metodo es default, seteo los otros como false
            if request.es_default:
                db.query(MetodoPago).filter(
                    MetodoPago.es_default == True,
                    MetodoPago.usuario_id == request.usuario_id,
                    MetodoPago.id != metodo_existente.id,
                ).update({"es_default": False})
                metodo_existente.es_default = True

            metodo_existente.moneda_id = request.moneda_id
            db.commit()

            return create_payment_method_out(
                id=metodo_existente.id,
                usuario_id=metodo_existente.usuario_id,
                tipo_pago_id=metodo_existente.tipo_pago_id,
                moneda_id=metodo_existente.moneda_id,
                marca_pago_id=detalle_existente.marca_pago_id,
                gateway_pago_id=None,
                es_default=metodo_existente.es_default,
                identificador_wallet=None,
                ultimos_cuatro_digitos=detalle_existente.ultimos_cuatro_digitos,
                nombre_titular=detalle_existente.nombre_titular,
                fecha_vencimiento=detalle_existente.fecha_vencimiento,
                banco_id=detalle_existente.banco_id,
            )

        # Crear nuevo
        if request.es_default:
            db.query(MetodoPago).filter(
                MetodoPago.es_default == True, MetodoPago.usuario_id == request.usuario_id
            ).update({"es_default": False})

        detalle_tarjeta = MetodoPagoTarjeta(
            marca_pago_id=request.marca_pago_id,
            numero_tarjeta=request.nro_tarjeta,
            ultimos_cuatro_digitos=last4,
            fecha_vencimiento=request.fecha_vencimiento,
            nombre_titular=request.nombre_titular,
            banco_id=request.banco_id,
        )
        db.add(detalle_tarjeta)
        db.flush()

        mp = MetodoPago(
            usuario_id=request.usuario_id,
            tipo_pago_id=request.tipo_pago_id,
            moneda_id=request.moneda_id,
            es_default=request.es_default,
            metodo_pago_detalle_id=detalle_tarjeta.id,
        )
        db.add(mp)
        db.commit()
        return create_payment_method_out(
            id=mp.id,
            usuario_id=mp.usuario_id,
            tipo_pago_id=mp.tipo_pago_id,
            moneda_id=mp.moneda_id,
            marca_pago_id=detalle_tarjeta.marca_pago_id,
            gateway_pago_id=None,
            es_default=mp.es_default,
            identificador_wallet=None,
            ultimos_cuatro_digitos=detalle_tarjeta.ultimos_cuatro_digitos,
            nombre_titular=detalle_tarjeta.nombre_titular,
            fecha_vencimiento=detalle_tarjeta.fecha_vencimiento,
            banco_id=detalle_tarjeta.banco_id,
        )

    if is_billetera:
        # Campos requeridos para billetera
        missing = []
        if not request.gateway_pago_id:
            missing.append("gateway_pago_id")
        if not request.identificador_wallet:
            missing.append("identificador_wallet")
        if not request.moneda_id:
            missing.append("moneda_id")
        if missing:
            raise HTTPException(status_code=400, detail=f"Faltan campos de billetera: {', '.join(missing)}")

        detalle_existente: MetodoPagoBilletera | None = (
            db.query(MetodoPagoBilletera)
            .filter(
                MetodoPagoBilletera.proveedor_id == request.gateway_pago_id,
                MetodoPagoBilletera.wallet_id == request.identificador_wallet,
            )
            .first()
        )

        metodo_existente: MetodoPago | None = None
        if detalle_existente:
            metodo_existente = (
                db.query(MetodoPago)
                .filter(
                    MetodoPago.usuario_id == request.usuario_id,
                    MetodoPago.tipo_pago_id == request.tipo_pago_id,
                    MetodoPago.metodo_pago_detalle_id == detalle_existente.id,
                )
                .first()
            )

        if metodo_existente:
            if metodo_existente.fecha_hora_baja is not None:
                metodo_existente.fecha_hora_baja = None
            if detalle_existente.fecha_hora_baja is not None:
                detalle_existente.fecha_hora_baja = None

            detalle_existente.moneda_id = request.moneda_id

            if request.es_default:
                db.query(MetodoPago).filter(
                    MetodoPago.es_default == True,
                    MetodoPago.usuario_id == request.usuario_id,
                    MetodoPago.id != metodo_existente.id,
                ).update({"es_default": False})
                metodo_existente.es_default = True

            metodo_existente.moneda_id = request.moneda_id
            db.commit()

            return create_payment_method_out(
                id=metodo_existente.id,
                usuario_id=metodo_existente.usuario_id,
                tipo_pago_id=metodo_existente.tipo_pago_id,
                moneda_id=metodo_existente.moneda_id,
                marca_pago_id=None,
                gateway_pago_id=detalle_existente.proveedor_id,
                es_default=metodo_existente.es_default,
                identificador_wallet=detalle_existente.wallet_id,
                ultimos_cuatro_digitos=None,
                nombre_titular=None,
                fecha_vencimiento=None,
                banco_id=None,
            )

        if request.es_default:
            db.query(MetodoPago).filter(
                MetodoPago.es_default == True, MetodoPago.usuario_id == request.usuario_id
            ).update({"es_default": False})

        billetera = MetodoPagoBilletera(
            proveedor_id=request.gateway_pago_id,
            wallet_id=request.identificador_wallet,
            moneda_id=request.moneda_id,
        )
        db.add(billetera)
        db.flush()

        mp = MetodoPago(
            usuario_id=request.usuario_id,
            tipo_pago_id=request.tipo_pago_id,
            moneda_id=request.moneda_id,
            es_default=request.es_default,
            metodo_pago_detalle_id=billetera.id,
        )
        db.add(mp)
        db.commit()
        return create_payment_method_out(
            id=mp.id,
            usuario_id=mp.usuario_id,
            tipo_pago_id=mp.tipo_pago_id,
            moneda_id=mp.moneda_id,
            marca_pago_id=None,
            gateway_pago_id=billetera.proveedor_id,
            es_default=mp.es_default,
            identificador_wallet=billetera.wallet_id,
            ultimos_cuatro_digitos=None,
            nombre_titular=None,
            fecha_vencimiento=None,
            banco_id=None,
        )

    raise HTTPException(status_code=400, detail="Tipo de método de pago no soportado.")


def get_payment_methods_logic(usuario_id: int, db: Session):
    metodos: list[MetodoPago] = (
        db.query(MetodoPago).filter(MetodoPago.usuario_id == usuario_id, MetodoPago.fecha_hora_baja == None).all()
    )

    out: list[get_payment_method] = []

    for mp in metodos:
        tipo: TipoMetodoPago | None = db.query(TipoMetodoPago).filter(TipoMetodoPago.id == mp.tipo_pago_id).first()
        nombre_tipo = tipo.nombre_metodo if tipo else None

        detalle_tarjeta: MetodoPagoTarjeta | None = None
        detalle_billetera: MetodoPagoBilletera | None = None

        if tipo and tipo.nombre_metodo.lower() in ("debito", "débito", "credito", "crédito"):
            detalle_tarjeta = (
                db.query(MetodoPagoTarjeta)
                .filter(
                    MetodoPagoTarjeta.id == mp.metodo_pago_detalle_id,
                    MetodoPagoTarjeta.fecha_hora_baja == None,
                )
                .first()
            )
        elif tipo and tipo.nombre_metodo.lower() == "billetera":
            detalle_billetera = (
                db.query(MetodoPagoBilletera)
                .filter(
                    MetodoPagoBilletera.id == mp.metodo_pago_detalle_id,
                    MetodoPagoBilletera.fecha_hora_baja == None,
                )
                .first()
            )
        else:
            detalle_tarjeta = (
                db.query(MetodoPagoTarjeta)
                .filter(
                    MetodoPagoTarjeta.id == mp.metodo_pago_detalle_id,
                    MetodoPagoTarjeta.fecha_hora_baja == None,
                )
                .first()
            )
            if detalle_tarjeta is None:
                detalle_billetera = (
                    db.query(MetodoPagoBilletera)
                    .filter(
                        MetodoPagoBilletera.id == mp.metodo_pago_detalle_id,
                        MetodoPagoBilletera.fecha_hora_baja == None,
                    )
                    .first()
                )

        nombre_marca = None
        nombre_gateway = None
        ultimos_cuatro = None
        nombre_titular = None
        fecha_vencimiento = None
        nombre_banco = None
        ident_wallet = None

        if detalle_tarjeta:
            marca = db.query(MarcaMetodoPago).filter(MarcaMetodoPago.id == detalle_tarjeta.marca_pago_id).first()
            banco = db.query(Banco).filter(Banco.id == detalle_tarjeta.banco_id).first()
            nombre_marca = marca.nombre_marca if marca else None
            ultimos_cuatro = detalle_tarjeta.ultimos_cuatro_digitos
            nombre_titular = detalle_tarjeta.nombre_titular
            fecha_vencimiento = detalle_tarjeta.fecha_vencimiento
            nombre_banco = banco.nombre_banco if banco else None

        if detalle_billetera:
            gateway = db.query(ProveedorBilletera).filter(ProveedorBilletera.id == detalle_billetera.proveedor_id).first()
            nombre_gateway = gateway.nombre_gateway if gateway else None
            ident_wallet = detalle_billetera.wallet_id

        out.append(
            get_payment_method(
                id=mp.id,
                usuario_id=mp.usuario_id,
                tipo_pago=nombre_tipo,
                marca_pago=nombre_marca,
                gateway_pago=nombre_gateway,
                es_default=mp.es_default,
                identificador_wallet=ident_wallet,
                ultimos_cuatro_digitos=ultimos_cuatro,
                nombre_titular=nombre_titular,
                fecha_vencimiento=fecha_vencimiento,
                banco=nombre_banco,
            )
        )

    return out


def update_payment_method_logic(pm_id: int, request: update_payment_method_req, db: Session):
    metodo_pago: MetodoPago | None = db.query(MetodoPago).filter(MetodoPago.id == pm_id).first()
    if metodo_pago is None:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado.")

    tipo_actual: TipoMetodoPago | None = db.query(TipoMetodoPago).filter(TipoMetodoPago.id == metodo_pago.tipo_pago_id).first()
    tipo_nuevo: TipoMetodoPago | None = db.query(TipoMetodoPago).filter(TipoMetodoPago.id == request.tipo_pago_id).first()
    if not tipo_nuevo:
        raise HTTPException(status_code=400, detail="Tipo de método de pago inválido.")

    is_billetera = tipo_nuevo.nombre_metodo.lower() == "billetera"
    is_tarjeta = tipo_nuevo.nombre_metodo.lower() in ("debito", "débito", "credito", "crédito")

    detalle_tarjeta_actual: MetodoPagoTarjeta | None = None
    detalle_billetera_actual: MetodoPagoBilletera | None = None

    if tipo_actual:
        tipo_actual_nombre = tipo_actual.nombre_metodo.lower()
        if tipo_actual_nombre in ("debito", "débito", "credito", "crédito"):
            detalle_tarjeta_actual = (
                db.query(MetodoPagoTarjeta)
                .filter(MetodoPagoTarjeta.id == metodo_pago.metodo_pago_detalle_id)
                .first()
            )
        elif tipo_actual_nombre == "billetera":
            detalle_billetera_actual = (
                db.query(MetodoPagoBilletera)
                .filter(MetodoPagoBilletera.id == metodo_pago.metodo_pago_detalle_id)
                .first()
            )
    else:
        detalle_tarjeta_actual = (
            db.query(MetodoPagoTarjeta)
            .filter(MetodoPagoTarjeta.id == metodo_pago.metodo_pago_detalle_id)
            .first()
        )
        if detalle_tarjeta_actual is None:
            detalle_billetera_actual = (
                db.query(MetodoPagoBilletera)
                .filter(MetodoPagoBilletera.id == metodo_pago.metodo_pago_detalle_id)
                .first()
            )

    if request.es_default is True:
        db.query(MetodoPago).filter(
            MetodoPago.es_default == True,
            MetodoPago.usuario_id == metodo_pago.usuario_id,
            MetodoPago.id != metodo_pago.id,
        ).update({"es_default": False})

    metodo_pago.tipo_pago_id = request.tipo_pago_id
    if request.moneda_id is not None:
        metodo_pago.moneda_id = request.moneda_id
    if request.es_default is not None:
        metodo_pago.es_default = request.es_default

    if is_tarjeta:
        if request.nro_tarjeta is not None and not request.nro_tarjeta.isdigit():
            raise HTTPException(status_code=400, detail="nro_tarjeta debe contener solo números.")

        missing = []
        marca_pago_id = request.marca_pago_id or (
            detalle_tarjeta_actual.marca_pago_id if detalle_tarjeta_actual else None
        )
        if not marca_pago_id:
            missing.append("marca_pago_id")

        nro_tarjeta_val = request.nro_tarjeta or (
            detalle_tarjeta_actual.numero_tarjeta if detalle_tarjeta_actual else None
        )
        if not nro_tarjeta_val:
            missing.append("nro_tarjeta")

        nombre_titular = request.nombre_titular or (
            detalle_tarjeta_actual.nombre_titular if detalle_tarjeta_actual else None
        )
        if not nombre_titular:
            missing.append("nombre_titular")

        fecha_vencimiento = request.fecha_vencimiento or (
            detalle_tarjeta_actual.fecha_vencimiento if detalle_tarjeta_actual else None
        )
        if not fecha_vencimiento:
            missing.append("fecha_vencimiento")

        banco_id = request.banco_id or (
            detalle_tarjeta_actual.banco_id if detalle_tarjeta_actual else None
        )
        if not banco_id:
            missing.append("banco_id")

        if missing:
            raise HTTPException(status_code=400, detail=f"Faltan campos de tarjeta: {', '.join(missing)}")

        last4 = nro_tarjeta_val[-4:]

        detalle_tarjeta_destino = detalle_tarjeta_actual
        if detalle_tarjeta_destino is None:
            detalle_tarjeta_destino = MetodoPagoTarjeta(
                marca_pago_id=marca_pago_id,
                numero_tarjeta=nro_tarjeta_val,
                ultimos_cuatro_digitos=last4,
                fecha_vencimiento=fecha_vencimiento,
                nombre_titular=nombre_titular,
                banco_id=banco_id,
            )
            db.add(detalle_tarjeta_destino)
            db.flush()
        else:
            detalle_tarjeta_destino.marca_pago_id = marca_pago_id
            detalle_tarjeta_destino.numero_tarjeta = nro_tarjeta_val
            detalle_tarjeta_destino.ultimos_cuatro_digitos = last4
            detalle_tarjeta_destino.fecha_vencimiento = fecha_vencimiento
            detalle_tarjeta_destino.nombre_titular = nombre_titular
            detalle_tarjeta_destino.banco_id = banco_id

        detalle_tarjeta_destino.fecha_hora_baja = None

        if detalle_billetera_actual and detalle_billetera_actual.fecha_hora_baja is None:
            detalle_billetera_actual.fecha_hora_baja = datetime.utcnow()

        metodo_pago.metodo_pago_detalle_id = detalle_tarjeta_destino.id

    elif is_billetera:
        missing = []
        gateway_id = request.gateway_pago_id or (
            detalle_billetera_actual.proveedor_id if detalle_billetera_actual else None
        )
        if not gateway_id:
            missing.append("gateway_pago_id")

        wallet_id = request.identificador_wallet or (
            detalle_billetera_actual.wallet_id if detalle_billetera_actual else None
        )
        if not wallet_id:
            missing.append("identificador_wallet")

        moneda_id = request.moneda_id or (
            detalle_billetera_actual.moneda_id if detalle_billetera_actual else metodo_pago.moneda_id
        )
        if not moneda_id:
            missing.append("moneda_id")

        if missing:
            raise HTTPException(status_code=400, detail=f"Faltan campos de billetera: {', '.join(missing)}")

        detalle_billetera_destino = detalle_billetera_actual
        if detalle_billetera_destino is None:
            detalle_billetera_destino = MetodoPagoBilletera(
                proveedor_id=gateway_id,
                wallet_id=wallet_id,
                moneda_id=moneda_id,
            )
            db.add(detalle_billetera_destino)
            db.flush()
        else:
            detalle_billetera_destino.proveedor_id = gateway_id
            detalle_billetera_destino.wallet_id = wallet_id
            detalle_billetera_destino.moneda_id = moneda_id

        detalle_billetera_destino.fecha_hora_baja = None

        if detalle_tarjeta_actual and detalle_tarjeta_actual.fecha_hora_baja is None:
            detalle_tarjeta_actual.fecha_hora_baja = datetime.utcnow()

        metodo_pago.metodo_pago_detalle_id = detalle_billetera_destino.id
        metodo_pago.moneda_id = moneda_id

    else:
        raise HTTPException(status_code=400, detail="Tipo de método de pago no soportado.")

    db.commit()

    detalle_tarjeta = None
    detalle_billetera = None
    if is_tarjeta:
        detalle_tarjeta = (
            db.query(MetodoPagoTarjeta)
            .filter(
                MetodoPagoTarjeta.id == metodo_pago.metodo_pago_detalle_id,
                MetodoPagoTarjeta.fecha_hora_baja == None,
            )
            .first()
        )
    elif is_billetera:
        detalle_billetera = (
            db.query(MetodoPagoBilletera)
            .filter(
                MetodoPagoBilletera.id == metodo_pago.metodo_pago_detalle_id,
                MetodoPagoBilletera.fecha_hora_baja == None,
            )
            .first()
        )
    else:
        detalle_tarjeta = (
            db.query(MetodoPagoTarjeta)
            .filter(
                MetodoPagoTarjeta.id == metodo_pago.metodo_pago_detalle_id,
                MetodoPagoTarjeta.fecha_hora_baja == None,
            )
            .first()
        )
        if detalle_tarjeta is None:
            detalle_billetera = (
                db.query(MetodoPagoBilletera)
                .filter(
                    MetodoPagoBilletera.id == metodo_pago.metodo_pago_detalle_id,
                    MetodoPagoBilletera.fecha_hora_baja == None,
                )
                .first()
            )

    nombre_marca_metodo = None
    nombre_gateway_metodo = None
    nombre_banco = None
    ultimos_cuatro = None
    nombre_titular = None
    fecha_vencimiento = None
    identificador_wallet = None

    if detalle_tarjeta:
        marca_metodo: MarcaMetodoPago | None = db.query(MarcaMetodoPago).filter(
            MarcaMetodoPago.id == detalle_tarjeta.marca_pago_id
        ).first()
        banco: Banco | None = db.query(Banco).filter(Banco.id == detalle_tarjeta.banco_id).first()
        nombre_marca_metodo = marca_metodo.nombre_marca if marca_metodo else None
        nombre_banco = banco.nombre_banco if banco else None
        ultimos_cuatro = detalle_tarjeta.ultimos_cuatro_digitos
        nombre_titular = detalle_tarjeta.nombre_titular
        fecha_vencimiento = detalle_tarjeta.fecha_vencimiento

    if detalle_billetera:
        gateway_metodo: ProveedorBilletera | None = db.query(ProveedorBilletera).filter(
            ProveedorBilletera.id == detalle_billetera.proveedor_id
        ).first()
        nombre_gateway_metodo = gateway_metodo.nombre_gateway if gateway_metodo else None
        identificador_wallet = detalle_billetera.wallet_id

    return get_payment_method(
        id=metodo_pago.id,
        usuario_id=metodo_pago.usuario_id,
        tipo_pago=tipo_nuevo.nombre_metodo,
        marca_pago=nombre_marca_metodo,
        gateway_pago=nombre_gateway_metodo,
        es_default=metodo_pago.es_default,
        identificador_wallet=identificador_wallet,
        ultimos_cuatro_digitos=ultimos_cuatro,
        nombre_titular=nombre_titular,
        fecha_vencimiento=fecha_vencimiento,
        banco=nombre_banco,
    )


def delete_payment_method_logic(pm_id: int, db: Session):
    metodo_pago: MetodoPago | None = db.query(MetodoPago).filter(MetodoPago.id == pm_id).first()

    if metodo_pago is None:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado.")

    if metodo_pago.es_default:
        raise HTTPException(status_code=400, detail="No se puede eliminar un método de pago por defecto.")

    metodo_pago.fecha_hora_baja = datetime.utcnow()

    # tipo_mp = metodo_pago.tipo_pago_id  # no usado actualmente

    db.commit()

    return {"detail": "Método de pago dado de baja correctamente."}


def cancel_payment_logic_controller(payment_id: int, db: Session):
    try:
        return cancel_payment_logic(payment_id, db)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

