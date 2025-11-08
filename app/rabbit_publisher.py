import asyncio
import json
import os
from pathlib import Path
from typing import Any, Mapping

import aio_pika
from aio_pika import Message, DeliveryMode
from dotenv import load_dotenv


# Cargar variables desde .env similar al consumer
env_path = Path(__file__).resolve().parents[2] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

RABBIT_URL = os.getenv("RABBITMQ_URL")

_connection: aio_pika.RobustConnection | None = None
_channel: aio_pika.abc.AbstractChannel | None = None


async def _ensure_channel() -> aio_pika.abc.AbstractChannel:
    global _connection, _channel
    if _connection is None or _connection.is_closed:
        if not RABBIT_URL:
            raise RuntimeError("RABBITMQ_URL no configurada")
        _connection = await aio_pika.connect_robust(RABBIT_URL)
    if _channel is None or _channel.is_closed:
        _channel = await _connection.channel()
        await _channel.set_qos(prefetch_count=10)
    return _channel


async def publish_json(
    queue_name: str,
    payload: Mapping[str, Any],
    *,
    ensure_queue: bool = True,
) -> None:
    """Publica un mensaje JSON de forma asíncrona en la cola indicada.

    Usa el default exchange con routing_key = queue_name.
    """
    # Conexión al broker
    channel = await _ensure_channel()

    # Si ensure_queue es true, aseguro que el mensaje es para tal cola
    if ensure_queue:
        await channel.declare_queue(queue_name, durable=True)

    # Creo el mensaje
    body = json.dumps(payload).encode("utf-8")
    message = Message(
        body=body,
        content_type="application/json",
        delivery_mode=DeliveryMode.PERSISTENT,
    )

    # Por defecto, se usa el exchange que envía según la routing key (cola)
    default_exchange = channel.default_exchange
    await default_exchange.publish(message, routing_key=queue_name)


def publish_message(queue_name: str, payload: Mapping[str, Any]) -> None:
    """Dispara la publicación sin bloquear la ejecución actual."""
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(publish_json(queue_name, payload))
    except RuntimeError:
        # Si no hay event loop (por ejemplo, en un hilo), ejecutar sincrónicamente
        asyncio.run(publish_json(queue_name, payload))


async def close() -> None:
    """Cierra canal y conexión si están abiertos."""
    global _channel, _connection
    try:
        if _channel and not _channel.is_closed:
            await _channel.close()
    finally:
        _channel = None
    try:
        if _connection and not _connection.is_closed:
            await _connection.close()
    finally:
        _connection = None

