from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class Moneda(Base):

    __tablename__ = "monedas"

    id = Column(Integer, primary_key=True, index=True)
    moneda_nombre = Column(String, nullable=False)
    fecha_hora_baja = Column(DateTime, nullable=True)
    fecha_hora_alta = Column(DateTime, default=datetime.utcnow)
    

