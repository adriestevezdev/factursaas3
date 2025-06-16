from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.middleware.auth import get_current_user
from app.models import PerfilEmpresa
from app.schemas.perfil_empresa import (
    PerfilEmpresaCreate, PerfilEmpresaUpdate, PerfilEmpresaResponse
)

router = APIRouter(
    prefix="/api/perfil-empresa",
    tags=["perfil-empresa"]
)


@router.get("", response_model=Optional[PerfilEmpresaResponse])
async def get_perfil_empresa(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene el perfil de empresa del usuario actual."""
    perfil = db.query(PerfilEmpresa).filter(
        PerfilEmpresa.user_id == current_user["user_id"]
    ).first()
    
    return perfil


@router.post("", response_model=PerfilEmpresaResponse)
async def create_perfil_empresa(
    perfil_data: PerfilEmpresaCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crea el perfil de empresa para el usuario actual."""
    # Verificar si ya existe un perfil
    existing_perfil = db.query(PerfilEmpresa).filter(
        PerfilEmpresa.user_id == current_user["user_id"]
    ).first()
    
    if existing_perfil:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un perfil de empresa para este usuario"
        )
    
    # Crear nuevo perfil
    db_perfil = PerfilEmpresa(
        **perfil_data.model_dump(),
        user_id=current_user["user_id"]
    )
    
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    
    return db_perfil


@router.put("", response_model=PerfilEmpresaResponse)
async def update_perfil_empresa(
    perfil_update: PerfilEmpresaUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza el perfil de empresa del usuario actual."""
    perfil = db.query(PerfilEmpresa).filter(
        PerfilEmpresa.user_id == current_user["user_id"]
    ).first()
    
    if not perfil:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el perfil de empresa"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = perfil_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(perfil, field, value)
    
    db.commit()
    db.refresh(perfil)
    
    return perfil


@router.delete("")
async def delete_perfil_empresa(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina el perfil de empresa del usuario actual."""
    perfil = db.query(PerfilEmpresa).filter(
        PerfilEmpresa.user_id == current_user["user_id"]
    ).first()
    
    if not perfil:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el perfil de empresa"
        )
    
    db.delete(perfil)
    db.commit()
    
    return {"detail": "Perfil de empresa eliminado exitosamente"}