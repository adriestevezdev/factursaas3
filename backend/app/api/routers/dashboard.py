from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.models.factura import Factura
from app.middleware.auth import get_current_user
from typing import Dict, Union

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
async def get_dashboard_stats(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Union[int, str]]:
    """
    Get dashboard statistics for the authenticated user.
    Returns counts of clients, products, and invoices.
    """
    # Count clients for this user
    clients_count = db.query(Cliente).filter(Cliente.user_id == current_user).count()
    
    # Count products for this user
    products_count = db.query(Producto).filter(Producto.user_id == current_user).count()
    
    # Count invoices for this user (if Factura model exists)
    invoices_count = 0
    try:
        invoices_count = db.query(Factura).filter(Factura.user_id == current_user).count()
    except Exception:
        # Factura model might not exist yet, so we'll default to 0
        invoices_count = 0
    
    return {
        "clients": clients_count,
        "products": products_count,
        "invoices": invoices_count,
        "user_id": current_user
    }

@router.get("/stats/test/{user_id}")
async def get_dashboard_stats_test(
    user_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Union[int, str]]:
    """
    Get dashboard statistics for a specific user (test endpoint, no auth required).
    Returns counts of clients, products, and invoices.
    """
    # Count clients for this user
    clients_count = db.query(Cliente).filter(Cliente.user_id == user_id).count()
    
    # Count products for this user
    products_count = db.query(Producto).filter(Producto.user_id == user_id).count()
    
    # Count invoices for this user (if Factura model exists)
    invoices_count = 0
    try:
        invoices_count = db.query(Factura).filter(Factura.user_id == user_id).count()
    except Exception:
        # Factura model might not exist yet, so we'll default to 0
        invoices_count = 0
    
    return {
        "clients": clients_count,
        "products": products_count,
        "invoices": invoices_count,
        "user_id": user_id
    }