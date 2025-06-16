from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.models.factura import Factura, LineaFactura, EstadoFactura
from decimal import Decimal
from datetime import date, timedelta
import logging
import random

logger = logging.getLogger(__name__)

# Consistent test user ID for all seed data
SEED_USER_ID = "user_test_seed_12345"

def get_sample_clients():
    """Generate sample client data with realistic Spanish business information"""
    return [
        {
            "nombre": "Construcciones García S.L.",
            "nif": "B12345678",
            "direccion": "Calle Mayor, 45",
            "ciudad": "Madrid",
            "codigo_postal": "28001",
            "pais": "España",
            "email": "admin@construccionesgarcia.es",
            "telefono": "+34 91 123 4567",
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Panadería El Trigo Dorado",
            "nif": "12345678Z",
            "direccion": "Plaza del Pan, 12",
            "ciudad": "Barcelona",
            "codigo_postal": "08001",
            "pais": "España",
            "email": "info@trigoDorado.es",
            "telefono": "+34 93 987 6543",
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Tecnología Avanzada S.A.",
            "nif": "A87654321",
            "direccion": "Polígono Industrial Norte, Nave 15",
            "ciudad": "Valencia",
            "codigo_postal": "46001",
            "pais": "España",
            "email": "ventas@tecavanzada.com",
            "telefono": "+34 96 456 7890",
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Restaurante Casa Pepe",
            "nif": "23456789A",
            "direccion": "Calle de la Comida, 8",
            "ciudad": "Sevilla",
            "codigo_postal": "41001",
            "pais": "España",
            "email": "reservas@casapepe.es",
            "telefono": "+34 95 234 5678",
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Autoservicio Los Pinos",
            "nif": "B98765432",
            "direccion": "Avenida de los Pinos, 234",
            "ciudad": "Bilbao",
            "codigo_postal": "48001",
            "pais": "España",
            "email": "contacto@lospinos.com",
            "telefono": "+34 94 876 5432",
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Floristería Bella Flor",
            "nif": "34567890B",
            "direccion": "Calle de las Flores, 67",
            "ciudad": "Granada",
            "codigo_postal": "18001",
            "pais": "España",
            "email": "pedidos@bellaflor.es",
            "telefono": "+34 95 567 8901",
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Consultoría Empresarial López",
            "nif": "45678901C",
            "direccion": "Torre Empresarial, Piso 12",
            "ciudad": "Zaragoza",
            "codigo_postal": "50001",
            "pais": "España",
            "email": "info@consultorialopez.com",
            "telefono": "+34 97 678 9012",
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Librería Cervantes",
            "nif": "56789012D",
            "direccion": "Plaza de la Literatura, 3",
            "ciudad": "Salamanca",
            "codigo_postal": "37001",
            "pais": "España",
            "email": "libros@cervantes.es",
            "telefono": "+34 92 789 0123",
            "user_id": SEED_USER_ID
        }
    ]

def get_sample_products():
    """Generate sample product/service data with realistic pricing and IVA"""
    return [
        {
            "nombre": "Consultoría de Desarrollo Web",
            "descripcion": "Servicio de consultoría para desarrollo de aplicaciones web modernas",
            "precio": Decimal("150.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": True,
            "codigo": "CONS-WEB-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Hosting Web Anual",
            "descripcion": "Servicio de alojamiento web con dominio incluido por 12 meses",
            "precio": Decimal("120.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": True,
            "codigo": "HOST-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Ordenador Portátil",
            "descripcion": "Portátil para oficina, 15.6 pulgadas, 8GB RAM, 256GB SSD",
            "precio": Decimal("650.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": False,
            "codigo": "PORT-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Licencia Software Contabilidad",
            "descripcion": "Licencia anual de software de contabilidad empresarial",
            "precio": Decimal("299.99"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": True,
            "codigo": "LIC-CONT-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Mesa de Oficina",
            "descripcion": "Mesa de oficina de madera, 120x80cm",
            "precio": Decimal("180.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": False,
            "codigo": "MESA-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Mantenimiento Mensual",
            "descripcion": "Servicio de mantenimiento mensual de equipos informáticos",
            "precio": Decimal("85.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": True,
            "codigo": "MANT-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Impresora Multifunción",
            "descripcion": "Impresora láser multifunción con WiFi",
            "precio": Decimal("320.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": False,
            "codigo": "IMP-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Formación en Excel",
            "descripcion": "Curso de formación en Excel avanzado (20 horas)",
            "precio": Decimal("250.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": True,
            "codigo": "FORM-EXC-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Monitor 24 pulgadas",
            "descripcion": "Monitor LED de 24 pulgadas Full HD",
            "precio": Decimal("199.99"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": False,
            "codigo": "MON-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Backup en la Nube",
            "descripcion": "Servicio de backup automático en la nube (100GB)",
            "precio": Decimal("45.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": True,
            "codigo": "BACK-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Teclado Inalámbrico",
            "descripcion": "Teclado inalámbrico ergonómico con ratón incluido",
            "precio": Decimal("55.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": False,
            "codigo": "TEC-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Auditoría de Seguridad",
            "descripcion": "Auditoría completa de seguridad informática",
            "precio": Decimal("500.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": True,
            "codigo": "AUD-SEC-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Disco Duro Externo 1TB",
            "descripcion": "Disco duro externo portátil de 1TB USB 3.0",
            "precio": Decimal("75.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": False,
            "codigo": "HDD-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Soporte Técnico Remoto",
            "descripcion": "Soporte técnico remoto por horas",
            "precio": Decimal("45.00"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": True,
            "codigo": "SUP-REM-001",
            "activo": True,
            "user_id": SEED_USER_ID
        },
        {
            "nombre": "Webcam HD",
            "descripcion": "Cámara web HD 1080p con micrófono integrado",
            "precio": Decimal("89.99"),
            "tipo_iva": Decimal("21.00"),
            "es_servicio": False,
            "codigo": "CAM-001",
            "activo": True,
            "user_id": SEED_USER_ID
        }
    ]

def seed_database():
    """Populate database with sample data"""
    db = SessionLocal()
    try:
        logger.info("Starting database seeding...")
        
        # Check if seed data already exists
        existing_clients = db.query(Cliente).filter(Cliente.user_id == SEED_USER_ID).count()
        existing_products = db.query(Producto).filter(Producto.user_id == SEED_USER_ID).count()
        existing_invoices = db.query(Factura).filter(Factura.user_id == SEED_USER_ID).count()
        
        if existing_clients > 0 or existing_products > 0 or existing_invoices > 0:
            logger.warning(f"Seed data already exists: {existing_clients} clients, {existing_products} products, {existing_invoices} invoices")
            return {"message": "Seed data already exists", "clients": existing_clients, "products": existing_products, "invoices": existing_invoices}
        
        # Insert sample clients
        clients_data = get_sample_clients()
        clients = []
        clients_created = 0
        for client_data in clients_data:
            client = Cliente(**client_data)
            db.add(client)
            db.flush()  # Ensure the database generates timestamps
            clients.append(client)
            clients_created += 1
        
        # Insert sample products
        products_data = get_sample_products()
        products = []
        products_created = 0
        for product_data in products_data:
            product = Producto(**product_data)
            db.add(product)
            db.flush()  # Ensure the database generates timestamps
            products.append(product)
            products_created += 1
        
        # Create sample invoices
        invoices_created = 0
        
        # Generate invoices for the last 3 months
        today = date.today()
        for i in range(12):  # Create 12 invoices
            invoice_date = today - timedelta(days=random.randint(1, 90))
            client = random.choice(clients)
            
            # Determine invoice status based on date
            if (today - invoice_date).days > 60:
                estado = EstadoFactura.PAGADA
            elif (today - invoice_date).days > 30:
                estado = EstadoFactura.ENVIADA
            else:
                estado = EstadoFactura.BORRADOR
            
            # Create invoice
            invoice = Factura(
                numero=f"2025-{i+1:04d}",
                fecha=invoice_date,
                cliente_id=client.id,
                estado=estado,
                user_id=SEED_USER_ID,
                notas="Factura generada automáticamente para pruebas"
            )
            
            # Add invoice lines (1-4 random products)
            num_lines = random.randint(1, 4)
            selected_products = random.sample(products, num_lines)
            
            subtotal = Decimal('0.00')
            total_iva = Decimal('0.00')
            
            for product in selected_products:
                cantidad = Decimal(str(random.randint(1, 5)))
                linea = LineaFactura(
                    producto_id=product.id,
                    descripcion=product.descripcion,
                    cantidad=cantidad,
                    precio_unitario=product.precio,
                    tipo_iva=product.tipo_iva,
                    subtotal=cantidad * product.precio
                )
                invoice.lineas.append(linea)
                
                subtotal += linea.subtotal
                total_iva += linea.subtotal * (linea.tipo_iva / 100)
            
            invoice.subtotal = subtotal
            invoice.total_iva = total_iva
            invoice.total = subtotal + total_iva
            
            db.add(invoice)
            invoices_created += 1
        
        db.commit()
        logger.info(f"Database seeded successfully: {clients_created} clients, {products_created} products, {invoices_created} invoices")
        
        return {
            "message": "Database seeded successfully",
            "clients_created": clients_created,
            "products_created": products_created,
            "invoices_created": invoices_created,
            "test_user_id": SEED_USER_ID
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

def cleanup_seed_data():
    """Remove all seed data from the database"""
    db = SessionLocal()
    try:
        logger.info("Starting seed data cleanup...")
        
        # Delete seed invoices (this will cascade delete invoice lines)
        invoices_deleted = db.query(Factura).filter(Factura.user_id == SEED_USER_ID).delete()
        
        # Delete seed clients
        clients_deleted = db.query(Cliente).filter(Cliente.user_id == SEED_USER_ID).delete()
        
        # Delete seed products
        products_deleted = db.query(Producto).filter(Producto.user_id == SEED_USER_ID).delete()
        
        db.commit()
        logger.info(f"Seed data cleaned up: {clients_deleted} clients, {products_deleted} products, {invoices_deleted} invoices deleted")
        
        return {
            "message": "Seed data cleaned up successfully",
            "clients_deleted": clients_deleted,
            "products_deleted": products_deleted,
            "invoices_deleted": invoices_deleted
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error cleaning up seed data: {e}")
        raise e
    finally:
        db.close()

def get_seed_stats():
    """Get statistics about seed data"""
    db = SessionLocal()
    try:
        clients_count = db.query(Cliente).filter(Cliente.user_id == SEED_USER_ID).count()
        products_count = db.query(Producto).filter(Producto.user_id == SEED_USER_ID).count()
        invoices_count = db.query(Factura).filter(Factura.user_id == SEED_USER_ID).count()
        
        return {
            "test_user_id": SEED_USER_ID,
            "clients": clients_count,
            "products": products_count,
            "invoices": invoices_count,
            "has_seed_data": clients_count > 0 or products_count > 0 or invoices_count > 0
        }
        
    finally:
        db.close()

if __name__ == "__main__":
    # Allow running the script directly for testing
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        result = cleanup_seed_data()
        print(result)
    else:
        result = seed_database()
        print(result)