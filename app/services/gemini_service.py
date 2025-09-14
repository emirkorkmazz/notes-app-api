import requests
import json
import re
from typing import Dict, Any, List
from app.config import settings

class GeminiService:
    """Gemini AI API ile etkileşim için service sınıfı"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
    def generate_content(self, note_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Not verilerini Gemini AI'ya göndererek analiz sonucu alır
        
        Args:
            note_data: Not verilerini içeren dictionary
            
        Returns:
            Gemini AI'dan gelen response
        """
        if not self.api_key:
            raise ValueError("Gemini API key bulunamadı. Lütfen .env dosyasında GEMINI_API_KEY'i tanımlayın.")
        
        # Not verilerini analiz etmek için prompt hazırla
        prompt = self._create_analysis_prompt(note_data)
        
        # Gemini API'ye gönderilecek payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        # Headers
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
        
        try:
            # API çağrısı yap
            response = requests.post(
                self.base_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            # Response'u kontrol et
            response.raise_for_status()
            
            # JSON response'u parse et
            result = response.json()
            
            # Gemini'dan gelen text'i extract et
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if len(parts) > 0 and 'text' in parts[0]:
                        analysis_text = parts[0]['text']
                        # Response'u parse et
                        parsed_analysis = self._parse_analysis_response(analysis_text)
                        return {
                            "success": True,
                            "analysis": parsed_analysis,
                            "raw_response": result
                        }
            
            return {
                "success": False,
                "error": "Gemini'dan beklenen formatta response alınamadı",
                "raw_response": result
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Gemini API çağrısı başarısız: {str(e)}",
                "raw_response": None
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Gemini response parse edilemedi: {str(e)}",
                "raw_response": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Beklenmeyen hata: {str(e)}",
                "raw_response": None
            }
    
    def _create_analysis_prompt(self, note_data: Dict[str, Any]) -> str:
        """
        Not verilerini analiz etmek için Gemini'ya gönderilecek prompt'u oluşturur
        
        Args:
            note_data: Not verilerini içeren dictionary
            
        Returns:
            Hazırlanmış prompt string'i
        """
        # Not verilerini string'e çevir
        note_title = note_data.get('title', 'Başlık yok')
        note_content = note_data.get('content', 'İçerik yok')
        note_tags = note_data.get('tags', [])
        note_pinned = note_data.get('pinned', False)
        start_date = note_data.get('start_date')
        end_date = note_data.get('end_date')
        
        # Tarih bilgilerini formatla
        date_info = ""
        if start_date:
            date_info += f"Başlangıç tarihi: {start_date}\n"
        if end_date:
            date_info += f"Bitiş tarihi: {end_date}\n"
        
        # Etiket bilgilerini formatla
        tags_info = ""
        if note_tags:
            tags_info = f"Etiketler: {', '.join(note_tags)}\n"
        
        # Sabitlenme durumu
        pinned_info = "Sabitlenmiş not" if note_pinned else "Normal not"
        
        prompt = f"""
Sen bir not analiz uzmanısın. Aşağıdaki not verilerini analiz et ve her zaman aynı formatta yanıt ver.

NOT VERİLERİ:
Başlık: {note_title}
İçerik: {note_content}
{pinned_info}
{date_info}{tags_info}

LÜTFEN AŞAĞIDAKİ FORMATTA YANIT VER (Her zaman aynı formatı kullan):

ANALİZ SONUCU:
- Not Türü: [Notun türünü belirle: Kişisel, İş, Alışveriş, Hatırlatma, vs.]
- Önem Seviyesi: [Düşük/Orta/Yüksek]
- Kategori: [Notun hangi kategoriye ait olduğunu belirle]
- Öneriler: [Not için 2-3 kısa öneri]
- Etiket Önerileri: [Mevcut etiketlere ek olarak önerilen etiketler]

ÖNEMLİ: Her zaman yukarıdaki formatı kullan ve kısa, öz yanıtlar ver. Analiz sonucunu JSON formatında değil, düz metin olarak ver.
"""
        
        return prompt.strip()
    
    def _parse_analysis_response(self, analysis_text: str) -> Dict[str, Any]:
        """
        Gemini AI'dan gelen analiz response'unu parse eder
        
        Args:
            analysis_text: Gemini'dan gelen ham analiz metni
            
        Returns:
            Parse edilmiş analiz verisi
        """
        try:
            # Varsayılan değerler
            parsed_data = {
                "note_type": "Belirsiz",
                "importance_level": "Orta",
                "category": "Genel",
                "suggestions": [],
                "suggested_tags": [],
                "raw_analysis": analysis_text
            }
            
            # Not Türü
            note_type_match = re.search(r'- Not Türü:\s*(.+)', analysis_text)
            if note_type_match:
                parsed_data["note_type"] = note_type_match.group(1).strip()
            
            # Önem Seviyesi
            importance_match = re.search(r'- Önem Seviyesi:\s*(.+)', analysis_text)
            if importance_match:
                parsed_data["importance_level"] = importance_match.group(1).strip()
            
            # Kategori
            category_match = re.search(r'- Kategori:\s*(.+)', analysis_text)
            if category_match:
                parsed_data["category"] = category_match.group(1).strip()
            
            # Öneriler
            suggestions_match = re.search(r'- Öneriler:\s*(.+?)(?=- Etiket Önerileri:|$)', analysis_text, re.DOTALL)
            if suggestions_match:
                suggestions_text = suggestions_match.group(1).strip()
                # Bullet point'leri ayır
                suggestions = re.findall(r'\*\s*(.+)', suggestions_text)
                parsed_data["suggestions"] = [s.strip() for s in suggestions if s.strip()]
            
            # Etiket Önerileri
            tags_match = re.search(r'- Etiket Önerileri:\s*(.+)', analysis_text)
            if tags_match:
                tags_text = tags_match.group(1).strip()
                # Virgülle ayrılmış etiketleri ayır
                parsed_data["suggested_tags"] = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
            
            return parsed_data
            
        except Exception as e:
            # Parse hatası durumunda ham metni döndür
            return {
                "note_type": "Parse Hatası",
                "importance_level": "Belirsiz",
                "category": "Genel",
                "suggestions": [],
                "suggested_tags": [],
                "raw_analysis": analysis_text,
                "parse_error": str(e)
            }

# Singleton instance
gemini_service = GeminiService()
