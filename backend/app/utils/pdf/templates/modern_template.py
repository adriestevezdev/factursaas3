from typing import Dict, Any
from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from .base_template import BaseInvoiceTemplate


class ModernInvoiceTemplate(BaseInvoiceTemplate):
    """Modern invoice template with clean design"""
    
    def __init__(self):
        super().__init__()
        self.primary_color = colors.HexColor("#2563eb")  # Blue
        self.accent_color = colors.HexColor("#1e40af")  # Darker blue
        self.text_color = colors.HexColor("#1f2937")  # Dark gray
        self.light_gray = colors.HexColor("#f3f4f6")
        
    def generate(self, invoice_data: Dict[str, Any], output: BytesIO) -> None:
        """Generate modern PDF invoice"""
        doc = SimpleDocTemplate(
            output,
            pagesize=A4,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        # Build the story
        story = []
        styles = self._get_custom_styles()
        
        # Header
        story.extend(self._create_header(invoice_data, styles))
        story.append(Spacer(1, 20))
        
        # Invoice info and client info side by side
        story.append(self._create_invoice_client_info(invoice_data, styles))
        story.append(Spacer(1, 30))
        
        # Line items
        story.append(self._create_line_items_table(invoice_data))
        story.append(Spacer(1, 20))
        
        # Totals
        story.append(self._create_totals_table(invoice_data))
        
        # Notes
        if invoice_data.get('notas'):
            story.append(Spacer(1, 30))
            story.append(self._create_notes_section(invoice_data, styles))
        
        # Footer
        story.append(Spacer(1, 40))
        story.append(self._create_footer(styles))
        
        # Build PDF
        doc.build(story)
    
    def _get_custom_styles(self):
        """Get custom paragraph styles"""
        styles = getSampleStyleSheet()
        
        # Company name style
        styles.add(ParagraphStyle(
            name='CompanyName',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=self.primary_color,
            spaceAfter=6,
            alignment=TA_LEFT
        ))
        
        # Invoice title style
        styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=styles['Heading1'],
            fontSize=32,
            textColor=self.primary_color,
            alignment=TA_RIGHT,
            spaceAfter=12
        ))
        
        # Section header style
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=self.accent_color,
            spaceAfter=6,
            spaceBefore=12
        ))
        
        # Normal text
        styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=self.text_color,
            leading=14
        ))
        
        return styles
    
    def _create_header(self, invoice_data: Dict[str, Any], styles):
        """Create invoice header"""
        elements = []
        
        # Company info from business profile
        empresa = invoice_data.get('empresa', {})
        company_data = [
            [f'<b>{empresa.get("nombre", "Tu Empresa S.L.")}</b>'],
        ]
        
        if empresa.get('direccion'):
            company_data.append([empresa['direccion']])
        
        ciudad_line = []
        if empresa.get('codigo_postal'):
            ciudad_line.append(empresa['codigo_postal'])
        if empresa.get('ciudad'):
            ciudad_line.append(empresa['ciudad'])
        if empresa.get('provincia'):
            ciudad_line.append(empresa['provincia'])
        if ciudad_line:
            company_data.append([', '.join(ciudad_line)])
        
        if empresa.get('nif'):
            company_data.append([f'NIF: {empresa["nif"]}'])
        if empresa.get('telefono'):
            company_data.append([f'Tel: {empresa["telefono"]}'])
        if empresa.get('email'):
            company_data.append([empresa['email']])
        if empresa.get('web'):
            company_data.append([empresa['web']])
        
        invoice_title_data = [
            [Paragraph('<b>FACTURA</b>', styles['InvoiceTitle'])],
            [Paragraph(f'<b>Nº {invoice_data["numero"]}</b>', styles['SectionHeader'])]
        ]
        
        # Create header table
        header_table = Table([
            [Table(company_data, colWidths=[200]), '', Table(invoice_title_data, colWidths=[200])]
        ], colWidths=[200, '*', 200])
        
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 14),
            ('TEXTCOLOR', (0, 0), (0, 0), self.primary_color),
        ]))
        
        elements.append(header_table)
        elements.append(HRFlowable(width="100%", thickness=2, color=self.primary_color, spaceAfter=20))
        
        return elements
    
    def _create_invoice_client_info(self, invoice_data: Dict[str, Any], styles):
        """Create invoice and client information section"""
        cliente = invoice_data['cliente']
        
        # Invoice details
        invoice_details = [
            ['<b>Fecha de Factura:</b>', datetime.fromisoformat(invoice_data['fecha'].replace('Z', '+00:00')).strftime('%d/%m/%Y')],
            ['<b>Estado:</b>', invoice_data['estado']],
        ]
        
        # Client details
        client_details = [
            [Paragraph('<b>Facturado a:</b>', styles['SectionHeader'])],
            [Paragraph(f'<b>{cliente["nombre"]}</b>', styles['CustomNormal'])],
            [Paragraph(f'NIF: {cliente["nif"]}', styles['CustomNormal'])],
            [Paragraph(cliente.get('direccion', ''), styles['CustomNormal'])],
        ]
        
        if cliente.get('email'):
            client_details.append([Paragraph(cliente['email'], styles['CustomNormal'])])
        if cliente.get('telefono'):
            client_details.append([Paragraph(cliente['telefono'], styles['CustomNormal'])])
        
        # Create info table
        info_table = Table([
            [Table(invoice_details, colWidths=[100, 100]), '', Table(client_details, colWidths=[200])]
        ], colWidths=[200, '*', 200])
        
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (2, 0), (2, 0), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (0, 0), self.light_gray),
            ('BACKGROUND', (2, 0), (2, 0), self.light_gray),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ]))
        
        return info_table
    
    def _create_line_items_table(self, invoice_data: Dict[str, Any]):
        """Create line items table"""
        # Table headers
        headers = ['Descripción', 'Cantidad', 'Precio Unit.', 'IVA', 'Subtotal']
        
        # Table data
        data = [headers]
        
        for linea in invoice_data['lineas']:
            data.append([
                linea['descripcion'],
                str(linea['cantidad']),
                self.format_currency(linea['precio_unitario']),
                self.format_percentage(linea['tipo_iva']),
                self.format_currency(linea['subtotal'])
            ])
        
        # Create table
        table = Table(data, colWidths=[250, 60, 80, 60, 80])
        
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
            ('LINEBELOW', (0, 0), (-1, 0), 2, self.primary_color),
            
            # Row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.light_gray]),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return table
    
    def _create_totals_table(self, invoice_data: Dict[str, Any]):
        """Create totals table"""
        data = [
            ['Subtotal:', self.format_currency(invoice_data['subtotal'])],
            ['IVA:', self.format_currency(invoice_data['total_iva'])],
            ['TOTAL:', self.format_currency(invoice_data['total'])],
        ]
        
        table = Table(data, colWidths=[400, 130])
        
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -2), 11),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('TEXTCOLOR', (0, -1), (-1, -1), self.primary_color),
            ('LINEABOVE', (0, -1), (-1, -1), 2, self.primary_color),
            ('TOPPADDING', (0, -1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ]))
        
        return table
    
    def _create_notes_section(self, invoice_data: Dict[str, Any], styles):
        """Create notes section"""
        elements = []
        elements.append(Paragraph('<b>Notas:</b>', styles['SectionHeader']))
        elements.append(Paragraph(invoice_data['notas'], styles['CustomNormal']))
        return KeepTogether(elements)
    
    def _create_footer(self, styles):
        """Create footer"""
        footer_text = "Gracias por su confianza. Para cualquier consulta, no dude en contactarnos."
        return Paragraph(f'<i>{footer_text}</i>', styles['CustomNormal'])