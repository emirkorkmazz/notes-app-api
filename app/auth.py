from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import db
from typing import Optional

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Mevcut kullanıcıyı Firebase ID token'dan al"""
    token = credentials.credentials
    
    user = await db.verify_user_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz Firebase ID token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_user_id(current_user: dict = Depends(get_current_user)) -> str:
    """Mevcut kullanıcının Firebase UID'sini al"""
    return current_user["id"]
