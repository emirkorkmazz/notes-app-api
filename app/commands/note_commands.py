from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from app.models.note_models import NoteCreateRequest, NoteUpdateRequest

@dataclass
class CreateNoteCommand:
    """Not oluşturma komutu"""
    note_data: NoteCreateRequest
    user_id: str

@dataclass
class UpdateNoteCommand:
    """Not güncelleme komutu"""
    note_id: UUID
    note_update: NoteUpdateRequest
    user_id: str

@dataclass
class DeleteNoteCommand:
    """Not silme komutu"""
    note_id: UUID
    user_id: str

@dataclass
class RestoreNoteCommand:
    """Not geri yükleme komutu"""
    note_id: UUID
    user_id: str

@dataclass
class GetNotesCommand:
    """Notları getirme komutu"""
    user_id: str

@dataclass
class GetNoteCommand:
    """Tek not getirme komutu"""
    note_id: UUID
    user_id: str

@dataclass
class AnalyzeNoteCommand:
    """Not analiz komutu"""
    note_id: UUID
    user_id: str
