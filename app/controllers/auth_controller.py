from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.models.auth_models import User, UserResponse, AuthStatusResponse, TokenRefreshResponse
from app.models.base import StandardResponse
from app.database import db
from app.auth import get_current_user

security = HTTPBearer()

class AuthController:
    """Authentication işlemleri controller'ı"""
    
    async def verify_token(self, credentials: HTTPAuthorizationCredentials) -> StandardResponse[User]:
        """Firebase ID token'ını doğrula ve kullanıcı bilgilerini döndür"""
        try:
            token = credentials.credentials
            user = await db.verify_user_token(token)
            
            if user is None:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="INVALID_TOKEN",
                    message="Geçersiz Firebase ID token",
                    data=None
                )
            
            user_data = User(
                id=user["id"],
                email=user["email"],
                created_at=user.get("created_at", None)
            )
            
            return StandardResponse(
                isSuccess=True,
                errorCode=None,
                message="Token başarıyla doğrulandı",
                data=user_data
            )
        except Exception as e:
            return StandardResponse(
                isSuccess=False,
                errorCode="TOKEN_VERIFICATION_ERROR",
                message=f"Token doğrulanamadı: {str(e)}",
                data=None
            )
    
    async def get_current_user_info(self, current_user: dict) -> StandardResponse[User]:
        """Mevcut kullanıcının bilgilerini getir"""
        user_data = User(
            id=current_user["id"],
            email=current_user["email"],
            created_at=current_user.get("created_at", None)
        )
        
        return StandardResponse(
            isSuccess=True,
            errorCode=None,
            message="Kullanıcı bilgileri başarıyla getirildi",
            data=user_data
        )
    
    async def refresh_token(self, credentials: HTTPAuthorizationCredentials) -> StandardResponse[dict]:
        """Token'ı yenile (Firebase'de otomatik olarak yapılır, bu endpoint bilgi amaçlı)"""
        try:
            token = credentials.credentials
            user = await db.verify_user_token(token)
            
            if user is None:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="INVALID_TOKEN",
                    message="Geçersiz Firebase ID token",
                    data=None
                )
            
            return StandardResponse(
                isSuccess=True,
                errorCode=None,
                message="Token geçerli",
                data={
                    "user_id": user["id"],
                    "note": "Firebase ID token'ları otomatik olarak yenilenir. Flutter uygulamanızda currentUser.getIdToken(true) kullanın."
                }
            )
        except Exception as e:
            # Token expired hatası için özel mesaj
            if "Token expired" in str(e):
                return StandardResponse(
                    isSuccess=False,
                    errorCode="TOKEN_EXPIRED",
                    message="Token süresi dolmuş. Lütfen Flutter uygulamanızda currentUser.getIdToken(true) ile yeni token alın.",
                    data=None
                )
            return StandardResponse(
                isSuccess=False,
                errorCode="TOKEN_REFRESH_ERROR",
                message=f"Token yenilenemedi: {str(e)}",
                data=None
            )
    
    async def get_auth_status(self) -> StandardResponse[dict]:
        """Authentication durumunu kontrol et (genel bilgi)"""
        return StandardResponse(
            isSuccess=True,
            errorCode=None,
            message="Firebase Authentication aktif",
            data={
                "note": "Giriş yapmak için Flutter uygulamanızda Firebase Authentication kullanın",
                "endpoints": {
                    "verify_token": "POST /api/v1/auth/verify-token - Token doğrula",
                    "get_user": "GET /api/v1/auth/me - Kullanıcı bilgileri",
                    "refresh_token": "POST /api/v1/auth/refresh-token - Token yenile"
                },
                "flutter_integration": {
                    "sign_in": "FirebaseAuth.instance.signInWithEmailAndPassword()",
                    "sign_up": "FirebaseAuth.instance.createUserWithEmailAndPassword()",
                    "get_token": "FirebaseAuth.instance.currentUser?.getIdToken(true)",
                    "sign_out": "FirebaseAuth.instance.signOut()"
                }
            }
        )