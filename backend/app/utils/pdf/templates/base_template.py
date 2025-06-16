from abc import ABC, abstractmethod
from typing import Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from io import BytesIO


class BaseInvoiceTemplate(ABC):
    """Base class for invoice PDF templates"""
    
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin = 50
        
    @abstractmethod
    def generate(self, invoice_data: Dict[str, Any], output: BytesIO) -> None:
        """Generate PDF invoice using the template
        
        Args:
            invoice_data: Dictionary containing all invoice information
            output: BytesIO buffer to write the PDF to
        """
        pass
    
    def format_currency(self, amount: float) -> str:
        """Format amount as currency"""
        return f"{amount:,.2f} €"
    
    def format_percentage(self, percentage: float) -> str:
        """Format percentage"""
        return f"{percentage}%"