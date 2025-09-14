# Note App API Test Case

FastAPI ile geliştirilmiş ölçeklendirebilir not alma API'si. Firebase Authentication, Firestore ve Gemini AI entegrasyonu ile.

## API Endpoints

### Authentication
- `POST /api/v1/auth/verify-token` - Firebase ID token doğrula
- `GET /api/v1/auth/me` - Kullanıcı bilgilerini getir
- `POST /api/v1/auth/refresh-token` - Token durumunu kontrol et
- `GET /api/v1/auth/status` - Auth durumu

### Notes
- `GET /api/v1/notes/` - Tüm notları getir
- `POST /api/v1/notes/` - Yeni not oluştur
- `GET /api/v1/notes/{id}` - Not detayı
- `PUT /api/v1/notes/{id}` - Not güncelle
- `DELETE /api/v1/notes/{id}` - Not sil
- `PATCH /api/v1/notes/{id}/restore` - Not geri yükle
- `GET /api/v1/notes/{id}/ai` - AI analiz

### Diğer
- `GET /` - Ana sayfa
- `GET /health` - Sağlık kontrolü
- `GET /docs` - Swagger UI

## Başlatma

### 1. Environment Ayarları
```bash
cp env.example .env
```

### 2. Requirements Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın
```bash
./start.sh
```

API `http://localhost:8000` adresinde çalışacaktır.

## API Dokümantasyonu

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Proje Yapısı

```
app/
├── controllers/     # Business logic
├── models/         # Data models (base, auth, notes)
├── routers/        # HTTP endpoints
├── commands/       # CQRS commands
├── queries/        # CQRS queries
└── services/       # External services
```

