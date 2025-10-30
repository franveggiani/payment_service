Payments Service (Microservicio de Pagos)

Servicio responsable de gestionar pagos de las compras, mantener los métodos de pago de los usuarios y propagar eventos de estado de pago de forma asíncrona mediante RabbitMQ.

**Responsabilidades**
- Procesa pagos de usuarios de compras.
- Notifica (async) el estado del pago para otros servicios como Orders y Stats.
- Permite cancelar un pago asociado a una orden.
- Mantiene los métodos/formas de pago habilitados por usuario.

**Stack Técnico**
- `FastAPI` para la API HTTP (`app/main.py`, `app/api.py`).
- `SQLAlchemy` + `Alembic` para ORM y migraciones.
- `PostgreSQL` (imagen PostGIS) como base de datos.
- `RabbitMQ` para mensajería asincrónica (`app/rabbit_consumer.py`).
- `aio-pika` para consumir colas.
- `Docker` y `docker compose` para orquestación.

**Estructura Relevante**
- API HTTP: `app/api.py:27`, `app/api.py:109`, `app/api.py:162`, `app/api.py:178`.
- Lógica de negocio de pagos: `app/services/payments.py`.
- Consumidores de RabbitMQ: `app/rabbit_consumer.py`.
- Modelos: `app/models/*` (pagos, estados, métodos, marcas, gateways, tipos).
- Configuración: `app/config.py`, variables en `.env`.
- Migraciones Alembic: `alembic/`, `alembic.ini`.
- Seeds de datos: `seeds/seed_payment_data.py`.

**Endpoints HTTP**
Prefijo común: `/api`
- `POST /api/create_payment` — Crea un pago. Body: `{ nro_cuenta, monto_pagado, order_id, metodo_pago_id }`.
- `GET /api/cancel_payment/{payment_id}` — Cancela un pago si su estado lo permite.
- `POST /api/create_payment_method` — Crea un método de pago del usuario.
- `GET /api/get_payment_methods/{usuario_id}` — Lista métodos de pago vigentes del usuario.
- `PATCH /api/update_payment_method/{pm_id}` — Actualiza un método de pago.
- `DELETE /api/delete_payment_method/{pm_id}` — Da de baja lógica un método (no si es default).

Ejemplos rápidos con curl:
- Crear pago: `curl -X POST http://localhost:8005/api/create_payment -H 'Content-Type: application/json' -d '{"nro_cuenta":"12345678","monto_pagado":1500.75,"order_id":42,"metodo_pago_id":1}'`
- Cancelar pago: `curl http://localhost:8005/api/cancel_payment/1`

**Mensajería Asíncrona (RabbitMQ)**
Consumidores:
- Cola `payments`: crea pagos a partir de mensajes con payload: `{ "nro_cuenta": "12345678", "monto_pagado": 1500.75, "order_id": 42, "metodo_pago_id": 1 }`
- Cola `payments_cancel`: cancela pagos a partir de mensajes con payload: `{ "payment_id": 1 }`

Archivo de ejemplos: `mensajes_rabbit`.

Nota sobre notificaciones: La publicación de eventos hacia otros servicios (Orders, Stats) está prevista en el diseño, pero no se observa lógica de publicación en este repositorio aún. Los puntos naturales para publicar serían tras crear/cancelar un pago en `app/services/payments.py`.

**Puesta en Marcha con Docker**
Pre-requisitos: Docker y Docker Compose instalados.
1) Configurar variables en `.env` (ya incluye valores por defecto):
   - `DATABASE_URL=postgresql+psycopg2://postgres:root@db:5432/payments`
   - `RABBIT_USER`, `RABBIT_PASSWORD`, `RABBITMQ_URL`
2) Levantar servicios base y aplicación: `docker compose up --build`
   - Levanta `db`, `rabbitmq`, corre el seeder `db-seeder`, inicia `backend` (API en `:8005`) y `consumer`.
3) Aplicar migraciones (si no se aplicaron previamente): `docker compose run --rm backend alembic upgrade head`
4) Semillas de catálogos (si necesitas re-ejecutar): `docker compose run --rm db-seeder`

Servicios expuestos:
- API HTTP: `http://localhost:8005`
- RabbitMQ Management UI: `http://localhost:15672` (usuario y password según `.env`)
- PostgreSQL: `localhost:5432`

**Ejecución Local (sin Docker)**
- Python 3.11+
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt`
- Exportar variables en `.env` o en el entorno (`DATABASE_URL`, `RABBITMQ_URL`, etc.)
- Migraciones: `alembic upgrade head`
- API: `uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload`
- Consumer: `python -m app.rabbit_consumer`

**Modelo de Datos (resumen)**
- `estado_pago`: catálogos de estados (En Proceso, Realizado, Fallido, Cancelado).
- `pagos`: registro de pagos (`nro_cuenta`, `monto_pagado`, `estado_actual`, `orden_id`, `metodo_pago_id`).
- `metodos_pago`: métodos por usuario (tipo, marca, gateway, default, wallet, últimos 4 dígitos).
- Catálogos: `tipos_metodos_pago`, `marcas_metodos_pago`, `gateways_metodos_pago`.
Seeds iniciales: ver `seeds/seed_payment_data.py`.

**Consideraciones y Buenas Prácticas**
- No almacenar PAN completo de tarjetas en texto plano en producción. El modelo actual permite `numero_tarjeta`; en entornos reales, tokenizar/guardar sólo últimos 4 dígitos y manejar el resto vía gateway.
- Validar y sanear inputs en los endpoints; ya se valida que `nro_tarjeta` contenga sólo números.
- Manejar idempotencia al consumir colas si se agregan publicaciones/confirmaciones.
- Añadir publicación de eventos a Orders/Stats tras transiciones de estado.

**Desarrollo**
- Código principal: `app/`
- Ejecutar tests/lint (si se agregan) desde el contenedor `backend`.
- Migraciones: `alembic revision -m "mensaje"` y `alembic upgrade head`.

**Licencia**
No especificada.

