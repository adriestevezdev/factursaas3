from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean
from app.db.database import Base
from app.models.base import TimestampMixin, UserOwnedMixin

class Producto(Base, TimestampMixin, UserOwnedMixin):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    tipo_iva = Column(Numeric(5, 2), default=21.00)
    es_servicio = Column(Boolean, default=False)
    codigo = Column(String(50))
    activo = Column(Boolean, default=True)