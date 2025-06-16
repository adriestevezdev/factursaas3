from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.factura import EstadoFactura

class LineaFacturaBase(BaseModel):
    producto_id: int
    descripcion: Optional[str] = None
    cantidad: Decimal = Field(..., gt=0, decimal_places=2)
    precio_unitario: Decimal = Field(..., ge=0, decimal_places=2)
    tipo_iva: Decimal = Field(..., ge=0, le=100, decimal_places=2)

class LineaFacturaCreate(LineaFacturaBase):
    pass

class LineaFacturaUpdate(LineaFacturaBase):
    producto_id: Optional[int] = None
    cantidad: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    precio_unitario: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    tipo_iva: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2)

class LineaFacturaResponse(LineaFacturaBase):
    id: int
    factura_id: int
    subtotal: Decimal
    
    class Config:
        from_attributes = True

class FacturaBase(BaseModel):
    cliente_id: int
    fecha: date
    estado: EstadoFactura = EstadoFactura.BORRADOR
    notas: Optional[str] = None

class FacturaCreate(FacturaBase):
    lineas: List[LineaFacturaCreate]

class FacturaUpdate(BaseModel):
    cliente_id: Optional[int] = None
    fecha: Optional[date] = None
    estado: Optional[EstadoFactura] = None
    notas: Optional[str] = None
    lineas: Optional[List[LineaFacturaCreate]] = None

class FacturaResponse(FacturaBase):
    id: int
    numero: str
    subtotal: Decimal
    total_iva: Decimal
    total: Decimal
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime]
    lineas: List[LineaFacturaResponse]
    
    class Config:
        from_attributes = True

class FacturaListResponse(BaseModel):
    id: int
    numero: str
    fecha: date
    cliente_id: int
    cliente_nombre: str
    total: Decimal
    estado: EstadoFactura
    created_at: datetime
    
    class Config:
        from_attributes = True