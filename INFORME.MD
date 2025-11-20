

# Microservicio de Pagos: Franco Veggiani

### Casos de uso

#### CU: Ver métodos de pago

- Precondición: Usuario con métodos de pago vigentes o no vigentes.
- Camino normal:
  - El usuario consulta sus métodos vigentes mediante `GET /api/get_payment_methods/{usuario_id}`.
  - El servicio devuelve una lista con información consolidada por método: tipo (débito/crédito/billetera), marca o gateway, últimos 4 dígitos, nombre del titular, banco, identificador de wallet y si es predeterminado.
- Caminos alternativos:
  - Si el usuario no tiene métodos vigentes, retorna lista vacía (200).
  - Si el tipo no puede inferirse por catálogo, se intenta resolver por el detalle asociado (tarjeta o billetera); si no hay detalle, el método no se incluye.

#### CU: Gestionar métodos de pago

- Precondición: El usuario autenticado necesita administrar los métodos de pago disponibles para cobros posteriores.
- Camino normal:
  - Alta: `POST /api/create_payment_method` con `tipo_pago_id` y `moneda_id`.
    - Tarjeta: requiere `marca_pago_id`, `nro_tarjeta`, `nombre_titular`, `fecha_vencimiento`, `banco_id`. Crea un detalle en `metodos_pago_tarjeta` y lo vincula por `metodo_pago_detalle_id`. Se guardan los últimos 4 dígitos.
    - Billetera: requiere `gateway_pago_id`, `identificador_wallet`, `moneda_id`. Crea el detalle en `metodos_pago_billetera` y lo vincula.
  - Default: si `es_default = true`, desactiva el default previo del usuario y marca el nuevo.
  - Modificación: `PATCH /api/update_payment_method/{pm_id}`. Puede actualizar campos principales y del detalle; si cambia el tipo, se crea un nuevo detalle y se da de baja el anterior.
  - Baja lógica: `DELETE /api/delete_payment_method/{pm_id}` para métodos que no son default.
- Caminos alternativos:
  - Faltan campos obligatorios según tipo: `400` con campos faltantes.
  - Si ya existe un método igual para el usuario (misma tarjeta/billetera), se reactiva y actualiza; se devuelve el método reactivado.
  - Intento de borrar un método default: `400`.

#### CU: Crear pago

- Endpoint: `POST /api/create_payment`
- Body: `{ nro_cuenta, monto_pagado, order_id, metodo_pago_id }`
- Resultado: crea un pago en estado “En Proceso” y publica evento de estado en la cola de salida.

#### CU: Cancelar pago

- Endpoint: `GET /api/cancel_payment/{payment_id}`
- Resultado: cambia el estado a “Cancelado” si el estado actual lo permite y publica evento de estado en la cola de salida.

- Nota (asíncrono relacionado): también puede actualizarse el estado vía cola `payments_set_status` con `status_id` o `new_status` ("Realizado" | "Fallido").

### Modelo de datos
Tablas de la base de datos (PostgreSQL)

**metodos_pago**

- id
- usuario_id
- tipo_pago_id
- moneda_id
- es_default
- fecha_hora_alta
- fecha_hora_baja
- metodo_pago_detalle_id


**metodos_pago_tarjeta**

- id
- marca_pago_id
- numero_tarjeta
- ultimos_cuatro_digitos
- fecha_vencimiento
- nombre_titular
- banco_id
- fecha_hora_alta
- fecha_hora_baja


**metodos_pago_billetera**

- id
- proveedor_id
- wallet_id
- moneda_id
- fecha_hora_alta
- fecha_hora_baja


**pagos**

- id
- fecha_hora_creacion
- estado_actual
- metodo_pago_id
- orden_id


**estado_pago**

- id
- fecha_hora_alta
- fecha_hora_baja
- nombre_estado


**tipos_metodos_pago**

- id
- fecha_hora_alta
- fecha_hora_baja
- nombre_metodo


**marcas_metodos_pago**

- id
- fecha_hora_alta
- fecha_hora_baja
- nombre_marca


**proveedores_billetera**

- id
- fecha_hora_alta
- fecha_hora_baja
- nombre_gateway


**monedas**

- id
- moneda_nombre
- fecha_hora_baja
- fecha_hora_alta


**bancos**

- id
- nombre_banco
- fecha_hora_baja
- fecha_hora_alta

### Interfaz REST (FastAPI)

#### Crear pagos `POST /api/create_payment`
Body: `create_payment_request` → `{ order_id: int, metodo_pago_id: int }`

```json
{
  "order_id": 4512,
  "metodo_pago_id": 98
}
```

#### Cancelar pagos `GET /api/cancel_payment/{payment_id}`
`GET /api/cancel_payment/{payment_id}`
```json
{
  "detail": "Pago cancelado correctamente."
}
```
#### Crear metodo de pago `POST /api/create_payment_method`
- `POST /api/create_payment_method`
  
**Crear metodo de pago con tarjeta**
```json
{
  "usuario_id": 52,
  "tipo_pago_id": 1,
  "moneda_id": 1,
  "marca_pago_id": 3,
  "nro_tarjeta": "4111111111111111",
  "nombre_titular": "Franco Veggiani",
  "fecha_vencimiento": "2026-02",
  "banco_id": 5,
  "es_default": true
}
```
**Crear metodo de pago con billetera**
```json
{
  "usuario_id": 52,
  "tipo_pago_id": 2,
  "moneda_id": 1,
  "gateway_pago_id": 4 //Ejemplo: MercadoPago,
  "identificador_wallet": "user52@wallet.com",
  "es_default": false
}
```
#### Obtener métodos de pago `GET /api/get_payment_methods/{usuario_id}`
Respuesta

```json
[
  {
    "metodo_pago_id": 321,
    "tipo_pago": "Tarjeta",
    "marca": "Visa",
    "ultimos_cuatro_digitos": "1111",
    "nombre_titular": "Franco Veggiani",
    "banco": "Banco Azul",
    "es_default": true
  },
  {
    "metodo_pago_id": 322,
    "tipo_pago": "Billetera",
    "gateway": "Mercado Pago",
    "identificador_wallet": "user52@wallet.com",
    "es_default": false
  }
]
```
#### `PATCH /api/update_payment_method/{pm_id}`
Petición
```http
PATCH /api/update_payment_method/322 HTTP/1.1
Content-Type: application/json

{
  "es_default": true
}
```
Respuesta
```json
{
  "metodo_pago_id": 322,
  "tipo_pago": "Billetera",
  "gateway": "Mercado Pago",
  "identificador_wallet": "user52@wallet.com",
  "es_default": true
}
```
#### `DELETE /api/delete_payment_method/{pm_id}`
Petición    
```http
DELETE /api/delete_payment_method/321 HTTP/1.1
```
Respuesta
  ```json
  {
    "detail": "Método de pago eliminado."
  }
  ```

### Interfaz asíncrona (RabbitMQ)

- Consumidores (`app/rabbit_consumer.py`):

#### Crear pagos (asíncrono)
Cola `payments`: crea pagos. Payload: `{ "order_id": 42, "metodo_pago_id": 1 }`.
  ```json
  {
    "order_id": 4512,
    "metodo_pago_id": 98
  }
  ```
#### Cancelar pagos (asíncrono)
Cola `payments_cancel`: cancela pagos. Payload: `{ "payment_id": 1 }`.
```json
{
  "payment_id": 732
}
  ```
#### Cambiar estado de pago
Cola `payments_set_status` (env `PAYMENTS_SET_STATUS_QUEUE`): cambia estado del pago.
- Por id: `{ "payment_id": 123, "status_id": 2 }`.
    ```json
    {
      "payment_id": 732,
      "status_id": 3
    }
    ```
- Por nombre: `{ "payment_id": 123, "new_status": "Realizado" }` o `"Fallido"`.
    ```json
    {
      "payment_id": 732,
      "new_status": "Realizado"
    }
    ```
- Publicación de eventos:
#### Publicar cambio de estado (topic)
Cola `payments_status`: emite `{ event: "payment_status_changed", payment_id, order_id, previous_status, new_status, changed_at }` al crear/cancelar/actualizar estado.
  ```json
  {
    "event": "payment_status_changed",
    "payment_id": 732,
    "order_id": 4512,
    "previous_status": "En Proceso",
    "new_status": "Realizado",
    "changed_at": "2024-06-12T14:48:00Z"
  }
  ```
