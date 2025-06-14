from sqlalchemy import Column, Integer, String, Text, Numeric, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.base import TimestampMixin, UserOwnedMixin
import enum

class EstadoFactura(str, enum.Enum):
    BORRADOR = "borrador"
    ENVIADA = "enviada"
    PAGADA = "pagada"
    CANCELADA = "cancelada"

class Factura(Base, TimestampMixin, UserOwnedMixin):
    __tablename__ = "facturas"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(50), nullable=False)
    fecha = Column(Date, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    
    subtotal = Column(Numeric(10, 2), default=0)
    total_iva = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), default=0)
    
    estado = Column(Enum(EstadoFactura), default=EstadoFactura.BORRADOR)
    notas = Column(Text)
    
    # Relaciones
    cliente = relationship("Cliente", backref="facturas")
    lineas = relationship("LineaFactura", back_populates="factura", cascade="all, delete-orphan")

class LineaFactura(Base):
    __tablename__ = "lineas_factura"
    
    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    
    descripcion = Column(Text)
    cantidad = Column(Numeric(10, 2), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    tipo_iva = Column(Numeric(5, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    
    # Relaciones
    factura = relationship("Factura", back_populates="lineas")
    producto = relationship("Producto")