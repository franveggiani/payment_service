import asyncio
import json
import os
from pathlib import Path
from typing import Any, Mapping

import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message
from dotenv import load_dotenv


# Cargar variables desde .env similar al consumer
env_path = Path(__file__).resolve().parents[2] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

RABBIT_URL = os.getenv("RABBITMQ_URL")
RABBIT_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "payments.events")

_connection: aio_pika.RobustConnection | None = None
_channel: aio_pika.abc.AbstractChannel | None = None
_exchange: aio_pika.abc.AbstractExchange | None = None

# ESTABLEZCO CONEXIÓN CON AIO_PIKA
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


async def _ensure_exchange() -> aio_pika.abc.AbstractExchange:
    """Declara (si hace falta) el exchange fanout/topic usado para notificar microservicios."""
    global _exchange
    channel = await _ensure_channel()
    if _exchange is None or _exchange.is_closed:
        _exchange = await channel.declare_exchange(
            RABBIT_EXCHANGE,
            ExchangeType.TOPIC,
            durable=True,
        )
    return _exchange


async def publish_json(
    routing_key: str,
    payload: Mapping[str, Any],
) -> None:
    """Publica un mensaje JSON en el exchange fanout/topic configurado."""
    # Cada microservicio (Orders, Stats, etc.) se liga con su cola al exchange
    exchange = await _ensure_exchange()

    # Creo el mensaje
    body = json.dumps(payload).encode("utf-8")
    message = Message(
        body=body,
        content_type="application/json",
        delivery_mode=DeliveryMode.PERSISTENT,
    )

    # Los servicios reciben el mensaje según el binding key de sus colas
    await exchange.publish(message, routing_key=routing_key)


def publish_message(routing_key: str, payload: Mapping[str, Any]) -> None:
    """Dispara la publicación sin bloquear la ejecución actual."""
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(publish_json(routing_key, payload))
    except RuntimeError:
        # Si no hay event loop (por ejemplo, en un hilo), ejecutar sincrónicamente
        asyncio.run(publish_json(routing_key, payload))


async def close() -> None:
    """Cierra canal y conexión si están abiertos."""
    global _channel, _connection, _exchange
    try:
        if _channel and not _channel.is_closed:
            await _channel.close()
    finally:
        _channel = None
        _exchange = None
    try:
        if _connection and not _connection.is_closed:
            await _connection.close()
    finally:
        _connection = None
