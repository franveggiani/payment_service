from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class Banco(Base):

    __tablename__ = "bancos"

    id = Column(Integer, primary_key=True, index=True)
    nombre_banco = Column(String, nullable=False)
    fecha_hora_baja = Column(DateTime, nullable=True)
    fecha_hora_alta = Column(DateTime, default=datetime.utcnow)
    

