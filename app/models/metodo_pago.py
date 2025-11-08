from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class MetodoPago(Base):

    __tablename__ = "metodos_pago"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    tipo_pago_id = Column(Integer, ForeignKey('tipos_metodos_pago.id'), nullable=False)
    moneda_id = Column(Integer, ForeignKey('monedas.id'), nullable=False)
    es_default = Column(Boolean, nullable=False, default=False)
    fecha_hora_baja = Column(DateTime, nullable=True)
    fecha_hora_alta = Column(DateTime, default=datetime.utcnow)
    metodo_pago_detalle_id = Column(Integer, nullable=False)
    
    tipos_metodo_pago = relationship("TipoMetodoPago")
    moneda = relationship("Moneda")
