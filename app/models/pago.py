from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime

class Pago(Base):

    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora_creacion = Column(DateTime, default=datetime.utcnow)
    estado_actual = Column(Integer, ForeignKey('estado_pago.id'), nullable=False)
    metodo_pago_id = Column(Integer, ForeignKey('metodos_pago.id'), nullable=False)
    orden_id = Column(Integer, nullable=False)

    estado_pago_list = relationship("EstadoPago")
    ordenes_pago = relationship("OrdenPago", back_populates="pago")
