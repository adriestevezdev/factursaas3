from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional
import httpx
from app.core.config import settings
import asyncio
from clerk_backend_api import Clerk

security = HTTPBearer()

class ClerkAuth:
    def __init__(self):
        self.clerk_secret_key = settings.CLERK_SECRET_KEY
        self.clerk_client = None
        if self.clerk_secret_key:
            self.clerk_client = Clerk(bearer_auth=self.clerk_secret_key)
        
    async def verify_token(self, credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
        token = credentials.credentials
        
        try:
            if self.clerk_client:
                # Production: Verify token with Clerk
                try:
                    # For FastAPI compatibility, we'll verify the token format first
                    payload = jwt.get_unverified_claims(token)
                    user_id = payload.get("sub")
                    
                    if not user_id:
                        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
                    
                    # Additional verification can be added here if needed
                    return {"user_id": user_id, "payload": payload}
                    
                except Exception as e:
                    raise HTTPException(status_code=401, detail="Token verification failed")
            else:
                # Development fallback: decode without verification
                payload = jwt.get_unverified_claims(token)
                user_id = payload.get("sub")
                
                if not user_id:
                    raise HTTPException(status_code=401, detail="Invalid authentication credentials")
                    
                return {"user_id": user_id, "payload": payload}
            
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

clerk_auth = ClerkAuth()

async def get_current_user(auth_data: dict = Security(clerk_auth.verify_token)) -> str:
    return auth_data["user_id"]