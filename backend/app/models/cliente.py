from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base
from app.models.base import TimestampMixin, UserOwnedMixin

class Cliente(Base, TimestampMixin, UserOwnedMixin):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    nif = Column(String(20))
    direccion = Column(Text)
    ciudad = Column(String(100))
    codigo_postal = Column(String(10))
    pais = Column(String(100), default="España")
    email = Column(String(200))
    telefono = Column(String(20))