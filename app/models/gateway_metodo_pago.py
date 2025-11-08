from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime

class ProveedorBilletera(Base):

    __tablename__ = "proveedores_billetera"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora_alta = Column(DateTime, default=datetime.utcnow)
    fecha_hora_baja = Column(DateTime, nullable=True)
    # Mantener alineado con su uso en seeds y API
    nombre_gateway = Column(String, nullable=False)
