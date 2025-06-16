from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from app.db.database import get_db
from app.middleware.auth import get_current_user
from app.core.billing import BillingService, PLAN_LIMITS

router = APIRouter(prefix="/api/billing", tags=["billing"])

@router.get("/plan")
async def get_user_plan(
    current_user: dict = Depends(get_current_user)
) -> Dict:
    """Get current user's plan information"""
    user_plan = BillingService.get_user_plan(current_user)
    plan_limits = BillingService.get_plan_limits(user_plan)
    
    return {
        "plan": user_plan,
        "limits": plan_limits,
        "features": plan_limits["features"]
    }

@router.get("/usage")
async def get_usage_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Dict:
    """Get current usage statistics"""
    user_id = current_user["user_id"]
    user_plan = BillingService.get_user_plan(current_user)
    
    usage = BillingService.get_usage_stats(db, user_id)
    limits = BillingService.get_plan_limits(user_plan)
    
    return {
        "plan": user_plan,
        "usage": usage,
        "limits": {
            "clientes": limits["clientes"],
            "facturas_por_mes": limits["facturas_por_mes"]
        }
    }

@router.get("/plans")
async def get_available_plans() -> Dict:
    """Get all available plans and their features"""
    return {
        "plans": [
            {
                "id": "free_user",
                "name": "Free",
                "price": 0,
                "limits": PLAN_LIMITS["free_user"]
            },
            {
                "id": "starter",
                "name": "Starter",
                "price": 9,
                "limits": PLAN_LIMITS["starter"]
            },
            {
                "id": "pro",
                "name": "Pro",
                "price": 29,
                "limits": PLAN_LIMITS["pro"]
            }
        ]
    }