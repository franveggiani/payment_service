from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class MetodoPago(Base):

    __tablename__ = "metodos_pago"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    tipo_pago_id = Column(Integer, ForeignKey('tipos_metodos_pago.id'), nullable=False)
    marca_pago_id = Column(Integer, ForeignKey('marcas_metodos_pago.id'), nullable=True)
    gateway_pago_id = Column(Integer, ForeignKey('gateways_metodos_pago.id'), nullable=True)
    es_default = Column(Boolean, nullable=False, default=False)
    identificador_wallet = Column(String, nullable=True)
    numero_tarjeta = Column(String, nullable=True)
    ultimos_cuatro_digitos = Column(String, nullable=True)
    fecha_hora_baja = Column(DateTime, nullable=True)
    fecha_hora_alta = Column(DateTime, default=datetime.utcnow)
    
    tipos_metodo_pago = relationship("TipoMetodoPago")
    marcas_metodos_pago = relationship("MarcaMetodoPago")
    gateways_metodos_pago = relationship("GatewayMetodoPago")

