from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime

class OrdenPago(Base):

    __tablename__ = "orden_pago"

    id = Column(Integer, primary_key=True, index=True)
    orden_externa_id = Column(Integer, nullable=False)
    id_pago = Column(Integer, ForeignKey('pagos.id'), nullable=False)
    id_estado_pago = Column(Integer, ForeignKey('estado_pago.id'), nullable=False)

    fecha_hora_alta = Column(DateTime, default=datetime.utcnow)
    fecha_hora_baja = Column(DateTime, nullable=True)
    nombre_estado = Column(String, nullable=False)

    pago = relationship("Pago", back_populates="ordenes_pago")
    estado_pago = relationship("EstadoPago")
