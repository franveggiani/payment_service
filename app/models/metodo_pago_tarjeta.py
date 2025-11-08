from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class MetodoPagoTarjeta(Base):

    __tablename__ = "metodos_pago_tarjeta"

    id = Column(Integer, primary_key=True, index=True)
    marca_pago_id = Column(Integer, ForeignKey('marcas_metodos_pago.id'), nullable=False)
    numero_tarjeta = Column(String, nullable=False)
    ultimos_cuatro_digitos = Column(String, nullable=True)
    fecha_vencimiento = Column(String, nullable=False)
    nombre_titular = Column(String, nullable=False)
    banco_id = Column(Integer, ForeignKey('bancos.id'), nullable=False)
    fecha_hora_baja = Column(DateTime, nullable=True)
    fecha_hora_alta = Column(DateTime, default=datetime.utcnow)
    
    marca = relationship("MarcaMetodoPago")
    banco = relationship("Banco")
