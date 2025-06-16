from functools import wraps
from typing import List, Optional
from fastapi import HTTPException, Depends
from app.middleware.auth import get_current_user
from app.core.billing import BillingService

def require_plan(allowed_plans: List[str]):
    """Decorator to check if user has one of the allowed plans"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=401, detail="Not authenticated")
            
            user_plan = BillingService.get_user_plan(current_user)
            
            if user_plan not in allowed_plans:
                raise HTTPException(
                    status_code=403, 
                    detail=f"Esta función requiere uno de los siguientes planes: {', '.join(allowed_plans)}. Tu plan actual es: {user_plan}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_feature(feature: str):
    """Decorator to check if user's plan has a specific feature"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=401, detail="Not authenticated")
            
            user_plan = BillingService.get_user_plan(current_user)
            
            if not BillingService.has_feature(user_plan, feature):
                raise HTTPException(
                    status_code=403, 
                    detail=f"Esta función requiere la característica '{feature}' que no está disponible en tu plan {user_plan}. Actualiza tu plan para acceder a esta función."
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

async def check_plan_limit(
    resource_type: str,
    current_user: dict = Depends(get_current_user)
) -> None:
    """Dependency to check plan limits before creating resources"""
    from app.db.database import get_db
    db = next(get_db())
    
    user_plan = BillingService.get_user_plan(current_user)
    user_id = current_user["user_id"]
    
    if resource_type == "cliente":
        can_create, error_message = BillingService.check_cliente_limit(db, user_id, user_plan)
    elif resource_type == "factura":
        can_create, error_message = BillingService.check_factura_limit(db, user_id, user_plan)
    else:
        raise ValueError(f"Unknown resource type: {resource_type}")
    
    if not can_create:
        raise HTTPException(status_code=403, detail=error_message)