from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional
import httpx
from app.core.config import settings

security = HTTPBearer()

class ClerkAuth:
    def __init__(self):
        self.clerk_secret_key = settings.CLERK_SECRET_KEY
        
    async def verify_token(self, credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
        token = credentials.credentials
        
        try:
            # For development, we'll decode without verification
            # In production, you should verify with Clerk's public keys
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