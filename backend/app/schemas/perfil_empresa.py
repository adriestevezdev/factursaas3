from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PerfilEmpresaBase(BaseModel):
    """Schema base para perfil de empresa"""
    nombre: str
    nif: str
    direccion: Optional[str] = None
    codigo_postal: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    pais: str = "España"
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    web: Optional[str] = None
    prefijo_factura: str = ""
    siguiente_numero: str = "1"
    formato_numero: str = "{year}-{number:04d}"
    iban: Optional[str] = None
    banco: Optional[str] = None
    texto_legal: Optional[str] = None
    condiciones_pago: Optional[str] = None


class PerfilEmpresaCreate(PerfilEmpresaBase):
    """Schema para crear perfil de empresa"""
    pass


class PerfilEmpresaUpdate(BaseModel):
    """Schema para actualizar perfil de empresa"""
    nombre: Optional[str] = None
    nif: Optional[str] = None
    direccion: Optional[str] = None
    codigo_postal: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    pais: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    web: Optional[str] = None
    prefijo_factura: Optional[str] = None
    siguiente_numero: Optional[str] = None
    formato_numero: Optional[str] = None
    iban: Optional[str] = None
    banco: Optional[str] = None
    texto_legal: Optional[str] = None
    condiciones_pago: Optional[str] = None


class PerfilEmpresaResponse(PerfilEmpresaBase):
    """Schema de respuesta para perfil de empresa"""
    id: int
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True