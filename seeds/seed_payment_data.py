import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app import models  # noqa: F401  # ensure models are loaded
from app.models.gateway_metodo_pago import ProveedorBilletera
from app.models.marca_metodo_pago import MarcaMetodoPago
from app.models.tipo_metodo_pago import TipoMetodoPago
from app.models.estado_pago import EstadoPago
from app.models.banco import Banco           # <-- NUEVO
from app.models.moneda import Moneda         # <-- NUEVO

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

        # Tipos de método
        for nombre_metodo in ("Debito", "Credito", "Billetera"):
            get_or_create(session, TipoMetodoPago, nombre_metodo=nombre_metodo)

        # Proveedores / Gateways de billetera
        for nombre_gateway in ("Paypal", "Mercado Pago"):
            get_or_create(session, ProveedorBilletera, nombre_gateway=nombre_gateway)

        # Marcas de tarjeta
        for nombre_marca in ("Visa", "Mastercard"):
            get_or_create(session, MarcaMetodoPago, nombre_marca=nombre_marca)

        # Estados de pago
        for nombre_estado in ("En Proceso", "Realizado", "Fallido", "Cancelado"):
            get_or_create(session, EstadoPago, nombre_estado=nombre_estado)

        # -------------------------
        # NUEVO: Bancos
        # -------------------------
        bancos_arg = (
            "Banco de la Nación Argentina",
            "Banco de la Provincia de Buenos Aires",
            "Banco Ciudad de Buenos Aires",
            "Banco Santander",
            "BBVA",
            "Banco Macro",
            "Banco Galicia",
            "ICBC",
            "HSBC",
            "Banco Credicoop",
        )
        for nombre_banco in bancos_arg:
            get_or_create(session, Banco, nombre_banco=nombre_banco)

        # -------------------------
        # NUEVO: Monedas
        # (usamos códigos comunes como nombre para consistencia)
        # -------------------------
        monedas = (
            "ARS",  # Peso argentino
            "USD",  # Dólar estadounidense
            "EUR",  # Euro
            "BRL",  # Real brasileño
            "CLP",  # Peso chileno
            "UYU",  # Peso uruguayo
            "PYG",  # Guaraní paraguayo
        )
        for moneda_nombre in monedas:
            get_or_create(session, Moneda, moneda_nombre=moneda_nombre)

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
