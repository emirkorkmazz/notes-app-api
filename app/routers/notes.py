from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.models.note_models import (
    NoteCreateRequest, NoteUpdateRequest, NoteResponse, AIAnalysisResponse
)
from app.models.base import StandardResponse
from app.controllers.note_controller import NoteController
from app.auth import get_current_user_id

router = APIRouter(prefix="/notes", tags=["notes"])
note_controller = NoteController()

@router.get("/", response_model=StandardResponse[List[NoteResponse]])
async def get_notes(user_id: str = Depends(get_current_user_id)):
    """Kullanıcının tüm notlarını getir"""
    return await note_controller.get_notes(user_id)

@router.post("/", response_model=StandardResponse[NoteResponse], status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreateRequest, user_id: str = Depends(get_current_user_id)):
    """
    Yeni not oluştur
    
    - **title**: Not başlığı (1-200 karakter arası)
    - **content**: Not içeriği (en az 1 karakter)
    - **start_date**: Notun/geçerliliğin başlangıç zamanı (opsiyonel)
    - **end_date**: Notun/geçerliliğin bitiş zamanı (opsiyonel)
    - **pinned**: Not sabitlenmiş mi? (varsayılan: false)
    - **tags**: Not etiketleri (opsiyonel)
    
    Kullanıcı kimlik doğrulaması gerektirir.
    """
    return await note_controller.create_note(note, user_id)

@router.get("/{note_id}", response_model=StandardResponse[NoteResponse])
async def get_note(note_id: UUID, user_id: str = Depends(get_current_user_id)):
    """Belirli bir notu getir"""
    return await note_controller.get_note(note_id, user_id)

@router.put("/{note_id}", response_model=StandardResponse[NoteResponse])
async def update_note(note_id: UUID, note_update: NoteUpdateRequest, user_id: str = Depends(get_current_user_id)):
    """
    Notu güncelle
    
    - **note_id**: Güncellenecek notun ID'si
    - **title**: Yeni not başlığı (opsiyonel, 1-200 karakter arası)
    - **content**: Yeni not içeriği (opsiyonel, en az 1 karakter)
    - **start_date**: Yeni başlangıç zamanı (opsiyonel)
    - **end_date**: Yeni bitiş zamanı (opsiyonel)
    - **pinned**: Sabitlenme durumu (opsiyonel)
    - **tags**: Yeni etiketler (opsiyonel)
    
    En az bir alan güncellenmelidir.
    Kullanıcı kimlik doğrulaması gerektirir.
    """
    return await note_controller.update_note(note_id, note_update, user_id)

@router.delete("/{note_id}", response_model=StandardResponse[None])
async def delete_note(note_id: UUID, user_id: str = Depends(get_current_user_id)):
    """Notu sil (soft delete)"""
    return await note_controller.delete_note(note_id, user_id)

@router.patch("/{note_id}/restore", response_model=StandardResponse[NoteResponse])
async def restore_note(note_id: UUID, user_id: str = Depends(get_current_user_id)):
    """Silinmiş notu geri yükle"""
    return await note_controller.restore_note(note_id, user_id)

@router.get("/{note_id}/ai", response_model=StandardResponse[AIAnalysisResponse])
async def analyze_note_with_ai(note_id: UUID, user_id: str = Depends(get_current_user_id)):
    """
    Notu Gemini AI ile analiz et
    
    - **note_id**: Analiz edilecek notun ID'si
    - Kullanıcı kimlik doğrulaması gerektirir
    - Not Firebase'den alınır ve Gemini AI'ya gönderilir
    - AI analiz sonucu döndürülür
    """
    return await note_controller.analyze_note_with_ai(note_id, user_id)
