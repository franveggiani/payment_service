import asyncio
import json
import logging
import os
from pathlib import Path

import aio_pika
from dotenv import load_dotenv

from app.session import SessionLocal
from app.schemes import create_payment_request
from app.services.payments import cancel_payment_logic, create_payment_logic

env_path = Path(__file__).resolve().parents[2] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

RABBIT_URL = os.getenv("RABBITMQ_URL")


async def consume_payments():
    connection = await _connect_with_retry()
    channel = await connection.channel()
    queue = await channel.declare_queue("payments", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                payload = json.loads(message.body)
                try:
                    with SessionLocal() as db:
                        create_payment_logic(create_payment_request(**payload), db)
                except Exception as exc:
                    logging.exception("Error procesando mensaje de pago: %s", payload)
                    raise


async def consume_order_cancel():
    connection = await _connect_with_retry()
    channel = await connection.channel()
    queue = await channel.declare_queue("payments_cancel", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                payload = json.loads(message.body)
                try:
                    with SessionLocal() as db:
                        payment_id = payload.get("payment_id")
                        if payment_id is None:
                            raise ValueError("Mensaje de cancelación sin payment_id.")
                        cancel_payment_logic(int(payment_id), db)
                except Exception as exc:
                    logging.exception("Error procesando cancelación de pago: %s", payload)
                    raise


async def main():
    await asyncio.gather(
        consume_payments(),
        consume_order_cancel(),
    )

async def _connect_with_retry(delay: int = 5):
    while True:
        try:
            return await aio_pika.connect_robust(RABBIT_URL)
        except Exception as exc:
            logging.warning("No se pudo conectar a RabbitMQ (%s). Reintentando en %s segundos...", exc, delay)
            await asyncio.sleep(delay)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    asyncio.run(main())
