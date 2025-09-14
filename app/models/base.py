from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar
from datetime import datetime
from uuid import UUID

# Generic type for data
T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    """Standart API response formatı"""
    isSuccess: bool = Field(..., description="İşlem başarılı mı?", example=True)
    errorCode: Optional[str] = Field(None, description="Hata kodu (varsa)", example="VALIDATION_ERROR")
    message: str = Field(..., description="İşlem mesajı", example="Kayıt başarılı")
    data: Optional[T] = Field(None, description="Dönen veri", example=None)

class BaseEntity(BaseModel):
    """Base entity modeli - tüm entityler için ortak alanlar"""
    id: UUID = Field(..., description="Entity ID'si")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")
    updated_at: datetime = Field(..., description="Güncellenme tarihi")
    
    class Config:
        from_attributes = True

class BaseUserEntity(BaseEntity):
    """Kullanıcı tabanlı entity modeli"""
    user_id: str = Field(..., description="Kullanıcı ID'si")
    deleted: bool = Field(False, description="Silinmiş mi? (soft delete)", example=False)

class BaseResponse(BaseModel):
    """Base response modeli - tüm response'lar için ortak alanlar"""
    pass
