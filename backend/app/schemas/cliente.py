from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    nif: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    codigo_postal: Optional[str] = None
    pais: str = "España"
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    nif: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    codigo_postal: Optional[str] = None
    pais: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class ClienteResponse(ClienteBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)