## HTTP (API REST)

### Ping básico
```
GET {{baseUrl}}/
```

### Crear método de pago - Tarjeta (default)
```
POST {{baseUrl}}/create_payment_method
Content-Type: application/json

{
  "usuario_id": 1,
  "tipo_pago_id": 2,
  "moneda_id": 1,
  "marca_pago_id": 1,
  "nro_tarjeta": "4111111111111111",
  "nombre_titular": "Franco Nicolas Veggiani",
  "fecha_vencimiento": "2026-12",
  "banco_id": 1,
  "es_default": true
}
```

### Crear método de pago - Billetera
```
POST {{baseUrl}}/create_payment_method
Content-Type: application/json

{
  "usuario_id": 1,
  "tipo_pago_id": 3,
  "moneda_id": 2,
  "gateway_pago_id": 2,
  "identificador_wallet": "franco.veggiani",
  "es_default": false
}
```

### Listar métodos vigentes del usuario
```
GET {{baseUrl}}/get_payment_methods/1
```

### Actualizar método (ej: poner billetera como default)
```
PATCH {{baseUrl}}/update_payment_method/{{pmBilletera}}
Content-Type: application/json

{
  "tipo_pago_id": 3,
  "moneda_id": 2,
  "gateway_pago_id": 2,
  "identificador_wallet": "user1.mercadopago",
  "es_default": true
}
```

### Borrar método (no default)
```
DELETE {{baseUrl}}/delete_payment_method/{{pmTarjeta}}
```

### Crear pago HTTP
```
POST {{baseUrl}}/create_payment
Content-Type: application/json

{
  "order_id": 5001,
  "metodo_pago_id": {{pmBilletera}}
}
```

### Cancelar pago HTTP
```
GET {{baseUrl}}/cancel_payment/{{paymentId}}
```

## RabbitMQ (colocar payloads en las colas)

Usa `rabbitmqadmin` o la UI de Rabbit (http://localhost:15672) para publicar en las colas. Ejemplo con Docker:
```
docker compose exec rabbitmq rabbitmqadmin publish routing_key=<cola> payload='<json>'
```

- **Crear pago** — cola `payments`  
  Payload:
  ```json
  { "order_id": 7001, "metodo_pago_id": 1 }
  ```

- **Cancelar pago** — cola `payments_cancel`  
  Payload:
  ```json
  { "payment_id": 1 }
  ```

- **Cambiar estado** — cola `payments_set_status` (env `PAYMENTS_SET_STATUS_QUEUE`)  
  Por id:
  ```json
  { "payment_id": 1, "status_id": 2 }
  ```
  Por nombre:
  ```json
  { "payment_id": 1, "new_status": "Realizado" }
  ```

- **Evento emitido por el servicio** — cola de salida `payments_status` (solo lectura, no publicar):  
  ```json
  {
    "event": "payment_status_changed",
    "payment_id": 1,
    "order_id": 7001,
    "previous_status": "En Proceso",
    "new_status": "Realizado",
    "changed_at": "2024-01-01T12:00:00Z"
  }
  ```
