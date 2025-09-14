from .base import StandardResponse, BaseEntity, BaseUserEntity, BaseResponse
from .auth_models import User, Token, TokenData, UserResponse, AuthStatusResponse, TokenRefreshResponse
from .note_models import (
    NoteBase, Note, NoteResponse, AIAnalysisResponse,
    NoteCreateRequest, NoteUpdateRequest
)

# Backward compatibility için eski modelleri export et
NoteCreate = NoteCreateRequest
NoteUpdate = NoteUpdateRequest

__all__ = [
    "StandardResponse", "BaseEntity", "BaseUserEntity", "BaseResponse",
    "User", "Token", "TokenData", "UserResponse", "AuthStatusResponse", "TokenRefreshResponse",
    "NoteBase", "Note", "NoteResponse", "AIAnalysisResponse",
    "NoteCreateRequest", "NoteUpdateRequest",
    "NoteCreate", "NoteUpdate"  # Backward compatibility
]
