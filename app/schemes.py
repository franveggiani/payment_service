from pydantic import BaseModel

class create_payment_request(BaseModel):
    nro_cuenta: str
    monto_pagado: float
    order_id: int
    metodo_pago_id: int

class create_payment_out(BaseModel):
    nro_cuenta: str
    monto_pagado: float
    estado: str

    class Config:
        orm_mode = True
        

class create_payment_method_req(BaseModel):
    usuario_id: int | None = None
    tipo_pago_id: int
    marca_pago_id: int | None = None
    gateway_pago_id: int | None = None
    es_default: bool
    identificador_wallet: str | None = None
    nro_tarjeta: str | None = None

class create_payment_method_out(BaseModel):
    id: int
    usuario_id: int | None = None
    tipo_pago_id: int
    marca_pago_id: int | None = None
    gateway_pago_id: int | None = None
    es_default: bool
    identificador_wallet: str | None = None
    ultimos_cuatro_digitos: str | None = None

    class Config:
        orm_mode = True

class get_payment_method(BaseModel):
    id: int
    usuario_id: int | None = None
    tipo_pago: str | None = None
    marca_pago: str | None = None
    gateway_pago: str | None = None
    es_default: bool
    identificador_wallet: str | None = None
    ultimos_cuatro_digitos: str | None = None

    class Config:
        orm_mode = True

class update_payment_method_req(BaseModel):
    tipo_pago_id: int
    marca_pago_id: int | None = None
    gateway_pago_id: int | None = None
    es_default: bool
    identificador_wallet: str | None = None
    nro_tarjeta: str | None = None
