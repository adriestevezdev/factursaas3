from typing import Dict, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.cliente import Cliente
from app.models.factura import Factura

# Plan configuration
PLAN_LIMITS = {
    "free_user": {
        "clientes": 5,
        "facturas_por_mes": 10,
        "features": {
            "pdf_export": False,
            "analytics": False,
            "custom_templates": False
        }
    },
    "starter": {
        "clientes": 50,
        "facturas_por_mes": 100,
        "features": {
            "pdf_export": True,
            "analytics": False,
            "custom_templates": False
        }
    },
    "pro": {
        "clientes": -1,  # Unlimited
        "facturas_por_mes": -1,  # Unlimited
        "features": {
            "pdf_export": True,
            "analytics": True,
            "custom_templates": True
        }
    }
}

class BillingService:
    """Service for handling billing and plan limits"""
    
    @staticmethod
    def get_user_plan(user_metadata: dict) -> str:
        """Extract user plan from JWT claims or metadata"""
        # First try to get plan from JWT claim (Clerk Billing)
        plan = user_metadata.get("plan")
        if plan:
            return plan
        
        # Fallback to publicMetadata if JWT claim not available
        return user_metadata.get("publicMetadata", {}).get("plan", "free_user")
    
    @staticmethod
    def get_plan_limits(plan: str) -> Dict:
        """Get limits for a specific plan"""
        return PLAN_LIMITS.get(plan, PLAN_LIMITS["free_user"])
    
    @staticmethod
    def check_cliente_limit(db: Session, user_id: str, user_plan: str) -> tuple[bool, Optional[str]]:
        """Check if user can create more clients"""
        limits = PLAN_LIMITS.get(user_plan, PLAN_LIMITS["free_user"])
        max_clientes = limits["clientes"]
        
        # Unlimited
        if max_clientes == -1:
            return True, None
        
        current_count = db.query(Cliente).filter(Cliente.user_id == user_id).count()
        
        if current_count >= max_clientes:
            return False, f"Has alcanzado el límite de {max_clientes} clientes en tu plan {user_plan}. Actualiza tu plan para añadir más clientes."
        
        return True, None
    
    @staticmethod
    def check_factura_limit(db: Session, user_id: str, user_plan: str) -> tuple[bool, Optional[str]]:
        """Check if user can create more invoices this month"""
        limits = PLAN_LIMITS.get(user_plan, PLAN_LIMITS["free_user"])
        max_facturas = limits["facturas_por_mes"]
        
        # Unlimited
        if max_facturas == -1:
            return True, None
        
        # Get current month's invoice count
        now = datetime.now(timezone.utc)
        start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        
        current_count = db.query(Factura).filter(
            Factura.user_id == user_id,
            Factura.created_at >= start_of_month
        ).count()
        
        if current_count >= max_facturas:
            return False, f"Has alcanzado el límite de {max_facturas} facturas este mes en tu plan {user_plan}. Actualiza tu plan para crear más facturas."
        
        return True, None
    
    @staticmethod
    def has_feature(user_plan: str, feature: str) -> bool:
        """Check if a plan has access to a specific feature"""
        limits = PLAN_LIMITS.get(user_plan, PLAN_LIMITS["free_user"])
        return limits["features"].get(feature, False)
    
    @staticmethod
    def get_usage_stats(db: Session, user_id: str) -> Dict:
        """Get current usage statistics for a user"""
        cliente_count = db.query(Cliente).filter(Cliente.user_id == user_id).count()
        
        # Get current month's invoice count
        now = datetime.now(timezone.utc)
        start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        
        factura_count = db.query(Factura).filter(
            Factura.user_id == user_id,
            Factura.created_at >= start_of_month
        ).count()
        
        return {
            "clientes": cliente_count,
            "facturas_este_mes": factura_count
        }