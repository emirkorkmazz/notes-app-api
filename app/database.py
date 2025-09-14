import firebase_admin
from firebase_admin import credentials, firestore, auth
from app.config import settings
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
import logging

# Firebase Admin SDK'yı başlat
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.get_firebase_credentials())
        firebase_admin.initialize_app(cred)
    db_client = firestore.client()
except Exception as e:
    logging.error(f"Firebase başlatılamadı: {e}")
    db_client = None

class Database:
    def __init__(self):
        self.db = db_client
        self.notes_collection = "notes"
    
    async def create_note(self, note_data: dict, user_id: str) -> dict:
        """Yeni not oluştur"""
        if not self.db:
            raise Exception("Firebase bağlantısı kurulamadı")
        
        note_id = str(uuid4())
        note = {
            "id": note_id,
            "user_id": user_id,
            "title": note_data["title"],
            "content": note_data["content"],
            "start_date": note_data.get("start_date"),
            "end_date": note_data.get("end_date"),
            "pinned": note_data.get("pinned", False),
            "deleted": False,
            "tags": note_data.get("tags"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        try:
            doc_ref = self.db.collection(self.notes_collection).document(note_id)
            doc_ref.set(note)
            return note
        except Exception as e:
            raise Exception(f"Not oluşturulamadı: {str(e)}")
    
    async def get_user_notes(self, user_id: str, include_deleted: bool = False) -> List[dict]:
        """Kullanıcının notlarını getir"""
        if not self.db:
            raise Exception("Firebase bağlantısı kurulamadı")
        
        try:
            notes_ref = self.db.collection(self.notes_collection)
            # Firestore composite index gerektirmemek için önce user_id'ye göre filtrele, sonra sırala
            query = notes_ref.where("user_id", "==", user_id)
            
            # Soft delete kontrolü
            if not include_deleted:
                query = query.where("deleted", "==", False)
            
            docs = query.stream()
            
            notes = []
            for doc in docs:
                note_data = doc.to_dict()
                # Firestore timestamp'lerini datetime'a çevir
                if 'created_at' in note_data:
                    note_data['created_at'] = note_data['created_at'].replace(tzinfo=None)
                if 'updated_at' in note_data:
                    note_data['updated_at'] = note_data['updated_at'].replace(tzinfo=None)
                if 'start_date' in note_data and note_data['start_date']:
                    note_data['start_date'] = note_data['start_date'].replace(tzinfo=None)
                if 'end_date' in note_data and note_data['end_date']:
                    note_data['end_date'] = note_data['end_date'].replace(tzinfo=None)
                notes.append(note_data)
            
            # Python tarafında pinned notları önce, sonra created_at'e göre sırala
            notes.sort(key=lambda x: (not x.get('pinned', False), x.get('created_at', datetime.min)), reverse=True)
            
            return notes
        except Exception as e:
            raise Exception(f"Notlar getirilemedi: {str(e)}")
    
    async def get_note_by_id(self, note_id: str, user_id: str, include_deleted: bool = False) -> Optional[dict]:
        """Belirli bir notu getir (sadece sahibi)"""
        if not self.db:
            raise Exception("Firebase bağlantısı kurulamadı")
        
        try:
            doc_ref = self.db.collection(self.notes_collection).document(note_id)
            doc = doc_ref.get()
            
            if doc.exists:
                note_data = doc.to_dict()
                # Sahiplik kontrolü
                if note_data.get("user_id") == user_id:
                    # Soft delete kontrolü
                    if not include_deleted and note_data.get("deleted", False):
                        return None
                    
                    # Firestore timestamp'lerini datetime'a çevir
                    if 'created_at' in note_data:
                        note_data['created_at'] = note_data['created_at'].replace(tzinfo=None)
                    if 'updated_at' in note_data:
                        note_data['updated_at'] = note_data['updated_at'].replace(tzinfo=None)
                    if 'start_date' in note_data and note_data['start_date']:
                        note_data['start_date'] = note_data['start_date'].replace(tzinfo=None)
                    if 'end_date' in note_data and note_data['end_date']:
                        note_data['end_date'] = note_data['end_date'].replace(tzinfo=None)
                    return note_data
            return None
        except Exception as e:
            raise Exception(f"Not getirilemedi: {str(e)}")
    
    async def update_note(self, note_id: str, user_id: str, update_data: dict) -> Optional[dict]:
        """Notu güncelle"""
        if not self.db:
            raise Exception("Firebase bağlantısı kurulamadı")
        
        try:
            # Önce notun var olup olmadığını ve sahiplik kontrolü yap
            existing_note = await self.get_note_by_id(note_id, user_id)
            if not existing_note:
                return None
            
            # None değerleri temizle (sadece güncellenecek alanları dahil et)
            clean_update_data = {k: v for k, v in update_data.items() if v is not None}
            clean_update_data["updated_at"] = datetime.utcnow()
            
            doc_ref = self.db.collection(self.notes_collection).document(note_id)
            doc_ref.update(clean_update_data)
            
            # Güncellenmiş notu getir
            updated_doc = doc_ref.get()
            if updated_doc.exists:
                note_data = updated_doc.to_dict()
                # Firestore timestamp'lerini datetime'a çevir
                if 'created_at' in note_data:
                    note_data['created_at'] = note_data['created_at'].replace(tzinfo=None)
                if 'updated_at' in note_data:
                    note_data['updated_at'] = note_data['updated_at'].replace(tzinfo=None)
                if 'start_date' in note_data and note_data['start_date']:
                    note_data['start_date'] = note_data['start_date'].replace(tzinfo=None)
                if 'end_date' in note_data and note_data['end_date']:
                    note_data['end_date'] = note_data['end_date'].replace(tzinfo=None)
                return note_data
            return None
        except Exception as e:
            raise Exception(f"Not güncellenemedi: {str(e)}")
    
    async def delete_note(self, note_id: str, user_id: str, soft_delete: bool = True) -> bool:
        """Notu sil (soft delete varsayılan)"""
        if not self.db:
            raise Exception("Firebase bağlantısı kurulamadı")
        
        try:
            # Önce notun var olup olmadığını ve sahiplik kontrolü yap
            existing_note = await self.get_note_by_id(note_id, user_id)
            if not existing_note:
                return False
            
            doc_ref = self.db.collection(self.notes_collection).document(note_id)
            
            if soft_delete:
                # Soft delete - sadece deleted flag'ini true yap
                doc_ref.update({
                    "deleted": True,
                    "updated_at": datetime.utcnow()
                })
            else:
                # Hard delete - notu tamamen sil
                doc_ref.delete()
            
            return True
        except Exception as e:
            raise Exception(f"Not silinemedi: {str(e)}")
    
    async def restore_note(self, note_id: str, user_id: str) -> bool:
        """Silinmiş notu geri yükle"""
        if not self.db:
            raise Exception("Firebase bağlantısı kurulamadı")
        
        try:
            # Önce notun var olup olmadığını ve sahiplik kontrolü yap (deleted notları dahil)
            existing_note = await self.get_note_by_id(note_id, user_id, include_deleted=True)
            if not existing_note or not existing_note.get("deleted", False):
                return False
            
            doc_ref = self.db.collection(self.notes_collection).document(note_id)
            doc_ref.update({
                "deleted": False,
                "updated_at": datetime.utcnow()
            })
            
            return True
        except Exception as e:
            raise Exception(f"Not geri yüklenemedi: {str(e)}")
    
    async def verify_user_token(self, token: str) -> Optional[dict]:
        """Kullanıcı token'ını doğrula"""
        try:
            decoded_token = auth.verify_id_token(token)
            return {
                "id": decoded_token["uid"],
                "email": decoded_token.get("email", "")
            }
        except auth.ExpiredIdTokenError:
            logging.error("Token süresi dolmuş")
            return None
        except auth.InvalidIdTokenError:
            logging.error("Geçersiz token")
            return None
        except Exception as e:
            logging.error(f"Token doğrulanamadı: {e}")
            return None

# Global database instance
db = Database()
