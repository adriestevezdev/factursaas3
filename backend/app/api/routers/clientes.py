from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.middleware.auth import get_current_user
from app.core.billing import BillingService

router = APIRouter(
    prefix="/api/clientes",
    tags=["clientes"]
)

@router.get("/", response_model=List[ClienteResponse])
def get_clientes(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all clients for the authenticated user"""
    clientes = db.query(Cliente).filter(
        Cliente.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return clientes

@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(
    cliente_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific client by ID"""
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.user_id == current_user["user_id"]
    ).first()
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente not found"
        )
    
    return cliente

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(
    cliente: ClienteCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new client"""
    # Check plan limits
    user_plan = BillingService.get_user_plan(current_user)
    can_create, error_message = BillingService.check_cliente_limit(
        db, current_user["user_id"], user_plan
    )
    
    if not can_create:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_message
        )
    
    db_cliente = Cliente(
        **cliente.model_dump(),
        user_id=current_user["user_id"]
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a client"""
    db_cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.user_id == current_user["user_id"]
    ).first()
    
    if not db_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente not found"
        )
    
    update_data = cliente_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cliente, field, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(
    cliente_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a client"""
    db_cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.user_id == current_user["user_id"]
    ).first()
    
    if not db_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente not found"
        )
    
    db.delete(db_cliente)
    db.commit()
    return None