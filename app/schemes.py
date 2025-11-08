from pydantic import BaseModel

class create_payment_request(BaseModel):
    order_id: int
    metodo_pago_id: int

class create_payment_out(BaseModel):
    payment_id: int
    order_id: int
    status: str

    class Config:
        orm_mode = True
        

class create_payment_method_req(BaseModel):
    usuario_id: int
    tipo_pago_id: int
    moneda_id: int
    # Tarjeta
    marca_pago_id: int | None = None
    nro_tarjeta: str | None = None
    nombre_titular: str | None = None
    fecha_vencimiento: str | None = None
    banco_id: int | None = None
    # Billetera
    gateway_pago_id: int | None = None
    identificador_wallet: str | None = None
    
    es_default: bool | None = None

class create_payment_method_out(BaseModel):
    id: int
    usuario_id: int
    tipo_pago_id: int
    moneda_id: int
    marca_pago_id: int | None = None
    gateway_pago_id: int | None = None
    es_default: bool
    identificador_wallet: str | None = None
    ultimos_cuatro_digitos: str | None = None
    nombre_titular: str | None = None
    fecha_vencimiento: str | None = None
    banco_id: int | None = None

    class Config:
        orm_mode = True

class get_payment_method(BaseModel):
    id: int
    usuario_id: int
    tipo_pago: str | None = None
    marca_pago: str | None = None
    gateway_pago: str | None = None
    es_default: bool
    identificador_wallet: str | None = None
    ultimos_cuatro_digitos: str | None = None
    nombre_titular: str | None = None
    fecha_vencimiento: str | None = None
    banco: str | None = None

    class Config:
        orm_mode = True

class update_payment_method_req(BaseModel):
    tipo_pago_id: int
    moneda_id: int | None = None
    marca_pago_id: int | None = None
    nro_tarjeta: str | None = None
    nombre_titular: str | None = None
    fecha_vencimiento: str | None = None
    banco_id: int | None = None
    gateway_pago_id: int | None = None
    identificador_wallet: str | None = None
    es_default: bool = False
