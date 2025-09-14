from dataclasses import dataclass
from typing import Optional
from fastapi.security import HTTPAuthorizationCredentials
from app.models.auth_models import User

@dataclass
class VerifyTokenCommand:
    """Token doğrulama komutu"""
    credentials: HTTPAuthorizationCredentials
    
@dataclass
class RefreshTokenCommand:
    """Token yenileme komutu"""
    credentials: HTTPAuthorizationCredentials

@dataclass
class GetCurrentUserCommand:
    """Mevcut kullanıcı bilgilerini getirme komutu"""
    current_user: dict
