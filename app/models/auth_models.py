from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.base import BaseResponse

class User(BaseModel):
    """Kullanıcı modeli"""
    id: str = Field(..., description="Kullanıcı ID'si", example="user123")
    email: str = Field(..., description="Kullanıcı email adresi", example="user@example.com")
    created_at: Optional[datetime] = Field(None, description="Hesap oluşturulma tarihi", example="2024-01-15T10:30:00")
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Token modeli"""
    access_token: str = Field(..., description="Erişim token'ı", example="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(..., description="Token tipi", example="Bearer")

class TokenData(BaseModel):
    """Token veri modeli"""
    user_id: Optional[str] = Field(None, description="Kullanıcı ID'si", example="user123")

# Request Models
class VerifyTokenRequest(BaseModel):
    """Token doğrulama request modeli"""
    pass  # Token header'dan gelir

class RefreshTokenRequest(BaseModel):
    """Token yenileme request modeli"""
    pass  # Token header'dan gelir

# Response Models
class UserResponse(BaseResponse):
    """Kullanıcı bilgileri response modeli"""
    user: User
    
class AuthStatusResponse(BaseResponse):
    """Auth durumu response modeli"""
    status: str
    endpoints: dict
    flutter_integration: dict
    
class TokenRefreshResponse(BaseResponse):
    """Token yenileme response modeli"""
    user_id: str
    note: str
