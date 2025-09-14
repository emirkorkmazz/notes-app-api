# Backward compatibility için eski imports'ları koruyalım
from .models.base import StandardResponse, BaseEntity, BaseUserEntity, BaseResponse
from .models.auth_models import User, Token, TokenData, UserResponse, AuthStatusResponse, TokenRefreshResponse
from .models.note_models import (
    NoteBase, Note, NoteResponse, AIAnalysisResponse,
    NoteCreateRequest, NoteUpdateRequest
)

# Backward compatibility
NoteCreate = NoteCreateRequest
NoteUpdate = NoteUpdateRequest

# Tüm modelleri export et
__all__ = [
    "StandardResponse", "BaseEntity", "BaseUserEntity", "BaseResponse",
    "User", "Token", "TokenData", "UserResponse", "AuthStatusResponse", "TokenRefreshResponse",
    "NoteBase", "Note", "NoteResponse", "AIAnalysisResponse",
    "NoteCreateRequest", "NoteUpdateRequest",
    "NoteCreate", "NoteUpdate"  # Backward compatibility
]
