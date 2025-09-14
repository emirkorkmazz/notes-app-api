from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.auth_models import User, UserResponse, AuthStatusResponse, TokenRefreshResponse
from app.models.base import StandardResponse
from app.controllers.auth_controller import AuthController
from app.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()
auth_controller = AuthController()

@router.post("/verify-token", response_model=StandardResponse[User])
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Firebase ID token'ını doğrula ve kullanıcı bilgilerini döndür
    
    - **Authorization**: Bearer token ile Firebase ID token gönderin
    
    Başarılı doğrulama sonrası kullanıcı bilgileri döndürülür.
    """
    return await auth_controller.verify_token(credentials)

@router.get("/me", response_model=StandardResponse[User])
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Mevcut kullanıcının bilgilerini getir"""
    return await auth_controller.get_current_user_info(current_user)

@router.post("/refresh-token", response_model=StandardResponse[dict])
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Token'ı yenile (Firebase'de otomatik olarak yapılır, bu endpoint bilgi amaçlı)"""
    return await auth_controller.refresh_token(credentials)

@router.get("/status", response_model=StandardResponse[dict])
async def auth_status():
    """Authentication durumunu kontrol et (genel bilgi)"""
    return await auth_controller.get_auth_status()
