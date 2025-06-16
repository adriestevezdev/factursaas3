from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base, UserOwnedMixin, TimestampMixin


class PerfilEmpresa(Base, UserOwnedMixin, TimestampMixin):
    """Modelo para el perfil de empresa del usuario"""
    __tablename__ = "perfiles_empresa"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos básicos de la empresa
    nombre = Column(String(200), nullable=False)
    nif = Column(String(20), nullable=False)
    direccion = Column(Text)
    codigo_postal = Column(String(10))
    ciudad = Column(String(100))
    provincia = Column(String(100))
    pais = Column(String(100), default="España")
    
    # Datos de contacto
    telefono = Column(String(20))
    email = Column(String(255))
    web = Column(String(255))
    
    # Configuración de facturación
    prefijo_factura = Column(String(10), default="")  # Ej: "FAC-", "2024-"
    siguiente_numero = Column(String(10), default="1")  # Número siguiente para facturas
    formato_numero = Column(String(50), default="{year}-{number:04d}")  # Formato de numeración
    
    # Datos bancarios (para mostrar en facturas)
    iban = Column(String(50))
    banco = Column(String(100))
    
    # Textos legales
    texto_legal = Column(Text)  # Texto legal para incluir en facturas
    condiciones_pago = Column(Text)  # Condiciones de pago predeterminadas
    
    def __repr__(self):
        return f"<PerfilEmpresa {self.nombre} - Usuario {self.user_id}>"