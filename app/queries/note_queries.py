from dataclasses import dataclass
from uuid import UUID

@dataclass
class GetNotesQuery:
    """Notları getirme sorgusu"""
    user_id: str

@dataclass
class GetNoteQuery:
    """Tek not getirme sorgusu"""
    note_id: UUID
    user_id: str
