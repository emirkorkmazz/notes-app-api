from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Union
from datetime import datetime
from uuid import UUID
from app.models.base import BaseUserEntity, BaseResponse

class NoteBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=200, 
        description="Not başlığı",
        example="Alışveriş Listesi"
    )
    content: str = Field(
        ..., 
        min_length=1, 
        description="Not içeriği",
        example="Süt, ekmek, yumurta alınacak"
    )
    start_date: Optional[Union[datetime, str]] = Field(
        None, 
        alias="startDate",
        description="Notun/geçerliliğin başlangıç zamanı",
        example="2025-09-12T09:00:00Z"
    )
    end_date: Optional[Union[datetime, str]] = Field(
        None, 
        alias="endDate",
        description="Notun/geçerliliğin bitiş zamanı",
        example="2025-09-12T17:00:00Z"
    )
    
    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if v is None:
            return None
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            # DD/MM/YYYY formatını parse et
            if '/' in v:
                try:
                    day, month, year = v.split('/')
                    return datetime(int(year), int(month), int(day))
                except ValueError:
                    pass
            # ISO formatını parse et
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                pass
        raise ValueError(f"Geçersiz tarih formatı: {v}")
    
    class Config:
        populate_by_name = True  # Hem alias hem de field name'i kabul et
    
    pinned: bool = Field(
        False, 
        description="Not sabitlenmiş mi?",
        example=False
    )
    tags: Optional[List[str]] = Field(
        None, 
        description="Not etiketleri",
        example=["work", "todo"]
    )

class Note(BaseUserEntity):
    """Veritabanından gelen tam not modeli"""
    title: str
    content: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    pinned: bool = False
    tags: Optional[List[str]] = None

class NoteResponse(BaseResponse):
    """API response için not modeli"""
    id: UUID = Field(..., description="Not ID'si", example="123e4567-e89b-12d3-a456-426614174000")
    title: str = Field(..., description="Not başlığı", example="Alışveriş Listesi")
    content: str = Field(..., description="Not içeriği", example="Süt, ekmek, yumurta alınacak")
    start_date: Optional[datetime] = Field(None, description="Notun/geçerliliğin başlangıç zamanı", example="2025-09-12T09:00:00Z")
    end_date: Optional[datetime] = Field(None, description="Notun/geçerliliğin bitiş zamanı", example="2025-09-12T17:00:00Z")
    pinned: bool = Field(False, description="Not sabitlenmiş mi?", example=False)
    deleted: bool = Field(False, description="Not silinmiş mi? (soft delete)", example=False)
    tags: Optional[List[str]] = Field(None, description="Not etiketleri", example=["work", "todo"])
    created_at: datetime = Field(..., description="Oluşturulma tarihi", example="2024-01-15T10:30:00")
    updated_at: datetime = Field(..., description="Güncellenme tarihi", example="2024-01-15T10:30:00")
    
    class Config:
        from_attributes = True

class AIAnalysisResponse(BaseModel):
    """AI analiz sonucu modeli"""
    note_type: str = Field(..., description="Not türü", example="İş")
    importance_level: str = Field(..., description="Önem seviyesi", example="Yüksek")
    category: str = Field(..., description="Kategori", example="Proje Yönetimi")
    suggestions: List[str] = Field(..., description="Öneriler", example=["Sunum içeriğini gözden geçir", "Bütçe raporunu kontrol et"])
    suggested_tags: List[str] = Field(..., description="Önerilen etiketler", example=["zaman çizelgesi", "görevler"])
    raw_analysis: str = Field(..., description="Ham analiz metni", example="ANALİZ SONUCU:\n- Not Türü: İş\n...")

# Request Models
class NoteCreateRequest(BaseModel):
    """Yeni not oluşturmak için kullanılan model"""
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=200, 
        description="Not başlığı",
        example="Alışveriş Listesi"
    )
    content: str = Field(
        ..., 
        min_length=1, 
        description="Not içeriği",
        example="Süt, ekmek, yumurta alınacak"
    )
    start_date: Optional[Union[datetime, str]] = Field(
        None, 
        alias="startDate",
        description="Notun/geçerliliğin başlangıç zamanı",
        example="2025-09-12T09:00:00Z"
    )
    end_date: Optional[Union[datetime, str]] = Field(
        None, 
        alias="endDate",
        description="Notun/geçerliliğin bitiş zamanı",
        example="2025-09-12T17:00:00Z"
    )
    pinned: bool = Field(
        False, 
        description="Not sabitlenmiş mi?",
        example=False
    )
    tags: Optional[List[str]] = Field(
        None, 
        description="Not etiketleri",
        example=["work", "todo"]
    )
    
    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if v is None:
            return None
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            # DD/MM/YYYY formatını parse et
            if '/' in v:
                try:
                    day, month, year = v.split('/')
                    return datetime(int(year), int(month), int(day))
                except ValueError:
                    pass
            # ISO formatını parse et
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                pass
        raise ValueError(f"Geçersiz tarih formatı: {v}")
    
    class Config:
        populate_by_name = True

class NoteUpdateRequest(BaseModel):
    """Not güncellemek için kullanılan model"""
    title: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=200, 
        description="Not başlığı",
        example="Güncellenmiş Alışveriş Listesi"
    )
    content: Optional[str] = Field(
        None, 
        min_length=1, 
        description="Not içeriği",
        example="Süt, ekmek, yumurta, peynir alınacak"
    )
    start_date: Optional[Union[datetime, str]] = Field(
        None, 
        alias="startDate",
        description="Notun/geçerliliğin başlangıç zamanı",
        example="2025-09-12T09:00:00Z"
    )
    end_date: Optional[Union[datetime, str]] = Field(
        None, 
        alias="endDate",
        description="Notun/geçerliliğin bitiş zamanı",
        example="2025-09-12T17:00:00Z"
    )
    pinned: Optional[bool] = Field(
        None, 
        description="Not sabitlenmiş mi?",
        example=False
    )
    tags: Optional[List[str]] = Field(
        None, 
        description="Not etiketleri",
        example=["work", "todo"]
    )
    
    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if v is None:
            return None
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            # DD/MM/YYYY formatını parse et
            if '/' in v:
                try:
                    day, month, year = v.split('/')
                    return datetime(int(year), int(month), int(day))
                except ValueError:
                    pass
            # ISO formatını parse et
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                pass
        raise ValueError(f"Geçersiz tarih formatı: {v}")
    
    class Config:
        populate_by_name = True
