from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.middleware.auth import get_current_user

router = APIRouter(
    prefix="/api/productos",
    tags=["productos"]
)

@router.get("/", response_model=List[ProductoResponse])
def get_productos(
    skip: int = 0,
    limit: int = 100,
    solo_activos: bool = True,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all products for the authenticated user"""
    query = db.query(Producto).filter(Producto.user_id == user_id)
    
    if solo_activos:
        query = query.filter(Producto.activo == True)
    
    productos = query.offset(skip).limit(limit).all()
    return productos

@router.get("/{producto_id}", response_model=ProductoResponse)
def get_producto(
    producto_id: int,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific product by ID"""
    producto = db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.user_id == user_id
    ).first()
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto not found"
        )
    
    return producto

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def create_producto(
    producto: ProductoCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new product"""
    db_producto = Producto(
        **producto.model_dump(),
        user_id=user_id
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.put("/{producto_id}", response_model=ProductoResponse)
def update_producto(
    producto_id: int,
    producto_update: ProductoUpdate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a product"""
    db_producto = db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.user_id == user_id
    ).first()
    
    if not db_producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto not found"
        )
    
    update_data = producto_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_producto, field, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(
    producto_id: int,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a product"""
    db_producto = db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.user_id == user_id
    ).first()
    
    if not db_producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto not found"
        )
    
    db.delete(db_producto)
    db.commit()
    return None