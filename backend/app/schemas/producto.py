from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    tipo_iva: Decimal = Decimal("21.00")
    es_servicio: bool = False
    codigo: Optional[str] = None
    activo: bool = True

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = None
    tipo_iva: Optional[Decimal] = None
    es_servicio: Optional[bool] = None
    codigo: Optional[str] = None
    activo: Optional[bool] = None

class ProductoResponse(ProductoBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)