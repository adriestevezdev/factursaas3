from typing import Dict, Any, Optional
from io import BytesIO
import base64
from sqlalchemy.orm import Session
from app.models import Factura, PerfilEmpresa
from .templates.modern_template import ModernInvoiceTemplate
from .templates.base_template import BaseInvoiceTemplate


class InvoiceGenerator:
    """Invoice PDF generator with template support"""
    
    TEMPLATES = {
        "modern": ModernInvoiceTemplate,
    }
    
    @classmethod
    def generate_pdf(cls, factura: Factura, template_name: str = "modern", perfil_empresa: Optional[PerfilEmpresa] = None) -> BytesIO:
        """Generate PDF for an invoice
        
        Args:
            factura: Factura model instance with loaded relations
            template_name: Name of the template to use
            
        Returns:
            BytesIO buffer containing the PDF
        """
        # Get template
        template_class = cls.TEMPLATES.get(template_name)
        if not template_class:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = template_class()
        
        # Prepare invoice data
        invoice_data = cls._prepare_invoice_data(factura, perfil_empresa)
        
        # Generate PDF
        output = BytesIO()
        template.generate(invoice_data, output)
        output.seek(0)
        
        return output
    
    @classmethod
    def generate_pdf_base64(cls, factura: Factura, template_name: str = "modern", perfil_empresa: Optional[PerfilEmpresa] = None) -> str:
        """Generate PDF and return as base64 string
        
        Args:
            factura: Factura model instance with loaded relations
            template_name: Name of the template to use
            
        Returns:
            Base64 encoded PDF string
        """
        pdf_buffer = cls.generate_pdf(factura, template_name, perfil_empresa)
        return base64.b64encode(pdf_buffer.read()).decode('utf-8')
    
    @classmethod
    def _prepare_invoice_data(cls, factura: Factura, perfil_empresa: Optional[PerfilEmpresa] = None) -> Dict[str, Any]:
        """Prepare invoice data for template
        
        Args:
            factura: Factura model instance
            
        Returns:
            Dictionary with all invoice data formatted for template
        """
        data = {
            "id": factura.id,
            "numero": factura.numero,
            "fecha": factura.fecha.isoformat(),
            "estado": factura.estado.value,
            "notas": factura.notas,
            "subtotal": float(factura.subtotal),
            "total_iva": float(factura.total_iva),
            "total": float(factura.total),
            "cliente": {
                "id": factura.cliente.id,
                "nombre": factura.cliente.nombre,
                "nif": factura.cliente.nif,
                "direccion": factura.cliente.direccion,
                "email": factura.cliente.email,
                "telefono": factura.cliente.telefono,
            },
            "lineas": [
                {
                    "id": linea.id,
                    "descripcion": linea.descripcion,
                    "cantidad": linea.cantidad,
                    "precio_unitario": float(linea.precio_unitario),
                    "tipo_iva": float(linea.tipo_iva),
                    "subtotal": float(linea.subtotal),
                }
                for linea in factura.lineas
            ]
        }
        
        # Add business profile data if available
        if perfil_empresa:
            data["empresa"] = {
                "nombre": perfil_empresa.nombre,
                "nif": perfil_empresa.nif,
                "direccion": perfil_empresa.direccion,
                "codigo_postal": perfil_empresa.codigo_postal,
                "ciudad": perfil_empresa.ciudad,
                "provincia": perfil_empresa.provincia,
                "pais": perfil_empresa.pais,
                "telefono": perfil_empresa.telefono,
                "email": perfil_empresa.email,
                "web": perfil_empresa.web,
                "iban": perfil_empresa.iban,
                "banco": perfil_empresa.banco,
                "texto_legal": perfil_empresa.texto_legal,
                "condiciones_pago": perfil_empresa.condiciones_pago,
            }
        else:
            # Default placeholder data
            data["empresa"] = {
                "nombre": "Tu Empresa S.L.",
                "nif": "B12345678",
                "direccion": "Calle Ejemplo 123",
                "codigo_postal": "28001",
                "ciudad": "Madrid",
                "provincia": "Madrid",
                "pais": "España",
                "telefono": "+34 900 123 456",
                "email": "email@tuempresa.com",
                "web": None,
                "iban": None,
                "banco": None,
                "texto_legal": None,
                "condiciones_pago": None,
            }
        
        return data
    
    @classmethod
    def get_available_templates(cls) -> list[str]:
        """Get list of available template names"""
        return list(cls.TEMPLATES.keys())