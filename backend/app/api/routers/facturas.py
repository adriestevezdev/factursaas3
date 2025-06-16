from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal

from app.db.database import get_db
from app.middleware.auth import get_current_user
from app.models import Factura, LineaFactura, Cliente, Producto
from app.schemas.factura import (
    FacturaCreate, FacturaUpdate, FacturaResponse, FacturaListResponse
)

router = APIRouter(
    prefix="/api/facturas",
    tags=["facturas"]
)

def generate_invoice_number(db: Session, user_id: str, year: int) -> str:
    """Genera el siguiente número de factura para un usuario y año específico."""
    # Obtener el último número de factura del usuario para ese año
    last_invoice = db.query(Factura).filter(
        Factura.user_id == user_id,
        extract('year', Factura.fecha) == year
    ).order_by(Factura.numero.desc()).first()
    
    if last_invoice and last_invoice.numero:
        # Extraer el número secuencial del formato YYYY-NNNN
        try:
            last_number = int(last_invoice.numero.split('-')[1])
            next_number = last_number + 1
        except:
            next_number = 1
    else:
        next_number = 1
    
    # Formato: YYYY-NNNN (ej: 2025-0001)
    return f"{year}-{next_number:04d}"

def calculate_invoice_totals(lineas: List[LineaFactura]) -> dict:
    """Calcula los totales de una factura basándose en sus líneas."""
    subtotal = Decimal('0.00')
    total_iva = Decimal('0.00')
    
    for linea in lineas:
        linea_subtotal = linea.cantidad * linea.precio_unitario
        linea_iva = linea_subtotal * (linea.tipo_iva / 100)
        
        subtotal += linea_subtotal
        total_iva += linea_iva
    
    total = subtotal + total_iva
    
    return {
        'subtotal': subtotal,
        'total_iva': total_iva,
        'total': total
    }

@router.get("/", response_model=List[FacturaListResponse])
async def get_facturas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    estado: Optional[str] = None,
    cliente_id: Optional[int] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene todas las facturas del usuario actual con filtros opcionales."""
    query = db.query(
        Factura.id,
        Factura.numero,
        Factura.fecha,
        Factura.cliente_id,
        Cliente.nombre.label('cliente_nombre'),
        Factura.total,
        Factura.estado,
        Factura.created_at
    ).join(Cliente).filter(Factura.user_id == current_user["user_id"])
    
    if estado:
        query = query.filter(Factura.estado == estado)
    if cliente_id:
        query = query.filter(Factura.cliente_id == cliente_id)
    if fecha_desde:
        query = query.filter(Factura.fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Factura.fecha <= fecha_hasta)
    
    facturas = query.order_by(Factura.fecha.desc(), Factura.id.desc()).offset(skip).limit(limit).all()
    
    return facturas

@router.get("/{factura_id}", response_model=FacturaResponse)
async def get_factura(
    factura_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene una factura específica del usuario actual."""
    factura = db.query(Factura).options(
        joinedload(Factura.lineas),
        joinedload(Factura.cliente)
    ).filter(
        Factura.id == factura_id,
        Factura.user_id == current_user["user_id"]
    ).first()
    
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    return factura

@router.post("/", response_model=FacturaResponse)
async def create_factura(
    factura_data: FacturaCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crea una nueva factura para el usuario actual."""
    # Verificar que el cliente pertenece al usuario
    cliente = db.query(Cliente).filter(
        Cliente.id == factura_data.cliente_id,
        Cliente.user_id == current_user["user_id"]
    ).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Verificar que todos los productos pertenecen al usuario
    producto_ids = [linea.producto_id for linea in factura_data.lineas]
    productos = db.query(Producto).filter(
        Producto.id.in_(producto_ids),
        Producto.user_id == current_user["user_id"]
    ).all()
    
    if len(productos) != len(producto_ids):
        raise HTTPException(status_code=404, detail="Uno o más productos no encontrados")
    
    # Generar número de factura
    year = factura_data.fecha.year
    numero = generate_invoice_number(db, current_user["user_id"], year)
    
    # Crear la factura
    db_factura = Factura(
        numero=numero,
        fecha=factura_data.fecha,
        cliente_id=factura_data.cliente_id,
        estado=factura_data.estado,
        notas=factura_data.notas,
        user_id=current_user["user_id"]
    )
    
    # Crear las líneas de factura
    for linea_data in factura_data.lineas:
        producto = next(p for p in productos if p.id == linea_data.producto_id)
        
        db_linea = LineaFactura(
            producto_id=linea_data.producto_id,
            descripcion=linea_data.descripcion or producto.nombre,
            cantidad=linea_data.cantidad,
            precio_unitario=linea_data.precio_unitario,
            tipo_iva=linea_data.tipo_iva,
            subtotal=linea_data.cantidad * linea_data.precio_unitario
        )
        db_factura.lineas.append(db_linea)
    
    # Calcular totales
    totales = calculate_invoice_totals(db_factura.lineas)
    db_factura.subtotal = totales['subtotal']
    db_factura.total_iva = totales['total_iva']
    db_factura.total = totales['total']
    
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    
    # Cargar relaciones para la respuesta
    db.refresh(db_factura)
    return db_factura

@router.put("/{factura_id}", response_model=FacturaResponse)
async def update_factura(
    factura_id: int,
    factura_update: FacturaUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza una factura existente del usuario actual."""
    factura = db.query(Factura).filter(
        Factura.id == factura_id,
        Factura.user_id == current_user["user_id"]
    ).first()
    
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # Actualizar campos básicos
    update_data = factura_update.dict(exclude_unset=True)
    
    # Si se cambia el cliente, verificar que pertenece al usuario
    if 'cliente_id' in update_data:
        cliente = db.query(Cliente).filter(
            Cliente.id == update_data['cliente_id'],
            Cliente.user_id == current_user["user_id"]
        ).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Si se actualizan las líneas, reemplazarlas completamente
    if 'lineas' in update_data:
        # Verificar que todos los productos pertenecen al usuario
        producto_ids = [linea.producto_id for linea in factura_update.lineas]
        productos = db.query(Producto).filter(
            Producto.id.in_(producto_ids),
            Producto.user_id == current_user["user_id"]
        ).all()
        
        if len(productos) != len(producto_ids):
            raise HTTPException(status_code=404, detail="Uno o más productos no encontrados")
        
        # Eliminar líneas existentes
        db.query(LineaFactura).filter(LineaFactura.factura_id == factura_id).delete()
        
        # Crear nuevas líneas
        nuevas_lineas = []
        for linea_data in factura_update.lineas:
            producto = next(p for p in productos if p.id == linea_data.producto_id)
            
            db_linea = LineaFactura(
                factura_id=factura_id,
                producto_id=linea_data.producto_id,
                descripcion=linea_data.descripcion or producto.nombre,
                cantidad=linea_data.cantidad,
                precio_unitario=linea_data.precio_unitario,
                tipo_iva=linea_data.tipo_iva,
                subtotal=linea_data.cantidad * linea_data.precio_unitario
            )
            nuevas_lineas.append(db_linea)
            db.add(db_linea)
        
        # Recalcular totales
        totales = calculate_invoice_totals(nuevas_lineas)
        factura.subtotal = totales['subtotal']
        factura.total_iva = totales['total_iva']
        factura.total = totales['total']
        
        # Eliminar 'lineas' del update_data para no intentar actualizarlo directamente
        del update_data['lineas']
    
    # Actualizar otros campos
    for field, value in update_data.items():
        setattr(factura, field, value)
    
    factura.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(factura)
    
    return factura

@router.delete("/{factura_id}")
async def delete_factura(
    factura_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina una factura del usuario actual."""
    factura = db.query(Factura).filter(
        Factura.id == factura_id,
        Factura.user_id == current_user["user_id"]
    ).first()
    
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    db.delete(factura)
    db.commit()
    
    return {"detail": "Factura eliminada exitosamente"}

# Test endpoints without authentication
@router.get("/test/{user_id}", response_model=List[FacturaListResponse])
async def get_facturas_test(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """TEST ENDPOINT: Obtiene todas las facturas de un usuario específico sin autenticación."""
    query = db.query(
        Factura.id,
        Factura.numero,
        Factura.fecha,
        Factura.cliente_id,
        Cliente.nombre.label('cliente_nombre'),
        Factura.total,
        Factura.estado,
        Factura.created_at
    ).join(Cliente).filter(Factura.user_id == user_id)
    
    facturas = query.order_by(Factura.fecha.desc(), Factura.id.desc()).offset(skip).limit(limit).all()
    
    return facturas