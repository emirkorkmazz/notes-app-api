from dataclasses import dataclass
from typing import Optional

@dataclass
class GetCurrentUserQuery:
    """Mevcut kullanıcı bilgilerini getirme sorgusu"""
    current_user: dict

@dataclass
class GetAuthStatusQuery:
    """Auth durumu sorgusu"""
    pass
