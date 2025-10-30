from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime

class EstadoPago(Base):

    __tablename__ = "estado_pago"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora_alta = Column(DateTime, default=datetime.utcnow)
    fecha_hora_baja = Column(DateTime, nullable=True)
    nombre_estado = Column(String, nullable=False)
