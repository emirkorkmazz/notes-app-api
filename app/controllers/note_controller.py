from fastapi import HTTPException, status
from typing import List
from uuid import UUID
from app.models.note_models import (
    NoteCreateRequest, NoteUpdateRequest, NoteResponse, AIAnalysisResponse
)
from app.models.base import StandardResponse
from app.database import db
from app.auth import get_current_user_id
from app.services.gemini_service import gemini_service

class NoteController:
    """Note işlemleri controller'ı"""
    
    async def get_notes(self, user_id: str) -> StandardResponse[List[NoteResponse]]:
        """Kullanıcının tüm notlarını getir"""
        try:
            notes = await db.get_user_notes(user_id)
            return StandardResponse(
                isSuccess=True,
                errorCode=None,
                message="Notlar başarıyla getirildi",
                data=notes
            )
        except Exception as e:
            return StandardResponse(
                isSuccess=False,
                errorCode="NOTES_FETCH_ERROR",
                message=f"Notlar getirilemedi: {str(e)}",
                data=None
            )
    
    async def create_note(self, note: NoteCreateRequest, user_id: str) -> StandardResponse[NoteResponse]:
        """Yeni not oluştur"""
        try:
            note_data = note.model_dump()
            created_note = await db.create_note(note_data, user_id)
            return StandardResponse(
                isSuccess=True,
                errorCode=None,
                message="Not başarıyla oluşturuldu",
                data=created_note
            )
        except Exception as e:
            return StandardResponse(
                isSuccess=False,
                errorCode="NOTE_CREATE_ERROR",
                message=f"Not oluşturulamadı: {str(e)}",
                data=None
            )
    
    async def get_note(self, note_id: UUID, user_id: str) -> StandardResponse[NoteResponse]:
        """Belirli bir notu getir"""
        try:
            note = await db.get_note_by_id(str(note_id), user_id)
            if not note:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="NOTE_NOT_FOUND",
                    message="Not bulunamadı veya erişim yetkiniz yok",
                    data=None
                )
            return StandardResponse(
                isSuccess=True,
                errorCode=None,
                message="Not başarıyla getirildi",
                data=note
            )
        except Exception as e:
            return StandardResponse(
                isSuccess=False,
                errorCode="NOTE_FETCH_ERROR",
                message=f"Not getirilemedi: {str(e)}",
                data=None
            )
    
    async def update_note(self, note_id: UUID, note_update: NoteUpdateRequest, user_id: str) -> StandardResponse[NoteResponse]:
        """Notu güncelle"""
        try:
            # Önce notun var olup olmadığını ve kullanıcının sahibi olup olmadığını kontrol et
            existing_note = await db.get_note_by_id(str(note_id), user_id)
            if not existing_note:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="NOTE_NOT_FOUND",
                    message="Not bulunamadı veya erişim yetkiniz yok",
                    data=None
                )
            
            # Sadece sağlanan alanları güncelle
            update_data = {k: v for k, v in note_update.model_dump().items() if v is not None}
            if not update_data:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="NO_UPDATE_DATA",
                    message="Güncellenecek veri bulunamadı",
                    data=None
                )
            
            updated_note = await db.update_note(str(note_id), user_id, update_data)
            if not updated_note:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="NOTE_UPDATE_ERROR",
                    message="Not güncellenemedi",
                    data=None
                )
            
            return StandardResponse(
                isSuccess=True,
                errorCode=None,
                message="Not başarıyla güncellendi",
                data=updated_note
            )
        except Exception as e:
            return StandardResponse(
                isSuccess=False,
                errorCode="NOTE_UPDATE_ERROR",
                message=f"Not güncellenemedi: {str(e)}",
                data=None
            )
    
    async def delete_note(self, note_id: UUID, user_id: str) -> StandardResponse[None]:
        """Notu sil (soft delete)"""
        try:
            # Önce notun var olup olmadığını ve kullanıcının sahibi olup olmadığını kontrol et
            existing_note = await db.get_note_by_id(str(note_id), user_id)
            if not existing_note:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="NOTE_NOT_FOUND",
                    message="Not bulunamadı veya erişim yetkiniz yok",
                    data=None
                )
            
            success = await db.delete_note(str(note_id), user_id, soft_delete=True)
            if not success:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="NOTE_DELETE_ERROR",
                    message="Not silinemedi",
                    data=None
                )
            
            return StandardResponse(
                isSuccess=True,
                errorCode=None,
                message="Not başarıyla silindi",
                data=None
            )
        except Exception as e:
            return StandardResponse(
                isSuccess=False,
                errorCode="NOTE_DELETE_ERROR",
                message=f"Not silinemedi: {str(e)}",
                data=None
            )
    
    async def restore_note(self, note_id: UUID, user_id: str) -> StandardResponse[NoteResponse]:
        """Silinmiş notu geri yükle"""
        try:
            success = await db.restore_note(str(note_id), user_id)
            if not success:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="NOTE_RESTORE_ERROR",
                    message="Not geri yüklenemedi veya bulunamadı",
                    data=None
                )
            
            # Geri yüklenen notu getir
            restored_note = await db.get_note_by_id(str(note_id), user_id)
            return StandardResponse(
                isSuccess=True,
                errorCode=None,
                message="Not başarıyla geri yüklendi",
                data=restored_note
            )
        except Exception as e:
            return StandardResponse(
                isSuccess=False,
                errorCode="NOTE_RESTORE_ERROR",
                message=f"Not geri yüklenemedi: {str(e)}",
                data=None
            )
    
    async def analyze_note_with_ai(self, note_id: UUID, user_id: str) -> StandardResponse[AIAnalysisResponse]:
        """Notu Gemini AI ile analiz et"""
        try:
            # Önce notun var olup olmadığını ve kullanıcının sahibi olup olmadığını kontrol et
            note = await db.get_note_by_id(str(note_id), user_id)
            if not note:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="NOTE_NOT_FOUND",
                    message="Not bulunamadı veya erişim yetkiniz yok",
                    data=None
                )
            
            # Not verilerini dictionary'ye çevir
            note_data = {
                "title": note.get("title", "Başlık yok"),
                "content": note.get("content", "İçerik yok"),
                "tags": note.get("tags", []),
                "pinned": note.get("pinned", False),
                "start_date": note.get("start_date").isoformat() if note.get("start_date") else None,
                "end_date": note.get("end_date").isoformat() if note.get("end_date") else None
            }
            
            # Gemini AI ile analiz yap
            ai_result = gemini_service.generate_content(note_data)
            
            if not ai_result["success"]:
                return StandardResponse(
                    isSuccess=False,
                    errorCode="AI_ANALYSIS_ERROR",
                    message=f"AI analizi başarısız: {ai_result.get('error', 'Bilinmeyen hata')}",
                    data=None
                )
            
            # Parse edilmiş analiz verisini AIAnalysisResponse modeline çevir
            analysis_data = ai_result["analysis"]
            ai_response = AIAnalysisResponse(
                note_type=analysis_data.get("note_type", "Belirsiz"),
                importance_level=analysis_data.get("importance_level", "Orta"),
                category=analysis_data.get("category", "Genel"),
                suggestions=analysis_data.get("suggestions", []),
                suggested_tags=analysis_data.get("suggested_tags", []),
                raw_analysis=analysis_data.get("raw_analysis", "")
            )
            
            return StandardResponse(
                isSuccess=True,
                errorCode=None,
                message="Not başarıyla AI ile analiz edildi",
                data=ai_response
            )
            
        except Exception as e:
            return StandardResponse(
                isSuccess=False,
                errorCode="AI_ANALYSIS_ERROR",
                message=f"AI analizi sırasında hata oluştu: {str(e)}",
                data=None
            )