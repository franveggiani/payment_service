from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class MetodoPagoBilletera(Base):

    __tablename__ = "metodos_pago_billetera"

    id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey('proveedores_billetera.id'), nullable=False)
    wallet_id = Column(String, nullable=True)
    fecha_hora_baja = Column(DateTime, nullable=True)
    fecha_hora_alta = Column(DateTime, default=datetime.utcnow)
    moneda_id = Column(Integer, ForeignKey('monedas.id'), nullable=False)
    
    gateways_metodos_pago = relationship("ProveedorBilletera")
    moneda = relationship("Moneda")