import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app import models  # noqa: F401  # ensure models are loaded
from app.models.gateway_metodo_pago import GatewayMetodoPago
from app.models.marca_metodo_pago import MarcaMetodoPago
from app.models.tipo_metodo_pago import TipoMetodoPago
from app.models.estado_pago import EstadoPago

logger = logging.getLogger(__name__)


def get_or_create(session, model, **filters):
    instance = session.query(model).filter_by(**filters).one_or_none()
    if instance is None:
        instance = model(**filters)
        session.add(instance)
        logger.info("Inserted %s - %s", model.__name__, filters)
    else:
        logger.info("Found existing %s - %s", model.__name__, filters)
    return instance


def main() -> None:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set.")

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)

    session = SessionLocal()
    try:
        logger.info("Seeding static payment method data.")

        for nombre_metodo in ("Debito", "Credito", "Billetera"):
            get_or_create(session, TipoMetodoPago, nombre_metodo=nombre_metodo)

        for nombre_gateway in ("Paypal", "Mercado Pago"):
            get_or_create(session, GatewayMetodoPago, nombre_gateway=nombre_gateway)

        for nombre_marca in ("Visa", "Mastercard"):
            get_or_create(session, MarcaMetodoPago, nombre_marca=nombre_marca)

        for nombre_estado in ("En Proceso", "Realizado", "Fallido", "Cancelado"):
            get_or_create(session, EstadoPago, nombre_estado=nombre_estado)

        session.commit()
        logger.info("Seed completed.")
    except SQLAlchemyError as exc:
        session.rollback()
        logger.error("Seed failed: %s", exc)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
